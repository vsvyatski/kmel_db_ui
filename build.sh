#!/bin/sh

case "$BASH" in
	*/bash)
		isBash=true
		;;
	*)
		isBash=false
		;;
esac

# Let's define some colors
if [ ${isBash} = true ]
then
	clr_red=$'\e[1;31m'
    clr_yellow=$'\e[1;33m'
	clr_end=$'\e[0m'
else
	clr_red=''
    clr_yellow=''
	clr_end=''
fi

usage() {
    echo 'Usage:'
    echo '  build.sh [options]'
    echo
    echo 'options:'
    echo '  -h                   display this help message and exit'
    echo '  -p <target_format>   pack build results into target format'
    echo '     supported formats:'
    echo "       tgz    - a *.tar.gz archive, it's distribution independent, but requires"
    echo '                manual installation'
    echo '       deb    - a *.deb package for Debian and derivatives'
    echo '       pacman - a *.pkg.tar.xz package for ArchLinux and derivatives'
}

checkFormat() {
    local format=$1
    test ${format} = tgz -o ${format} = deb -o ${format} = pacman
}

while getopts ":p:h" opt; do
	case ${opt} in
	    h)
	        usage
	        exit
	        ;;
		p)
			packageFormat=$OPTARG
			if ! checkFormat $packageFormat
			then
                printf "${clr_red}ERROR: Unrecognized target package format '$packageFormat'.${clr_end}\n" 1>&2
                usage
                exit 1
			fi
			;;
		\?)
			printf "${clr_red}ERROR: Unrecognized option -$OPTARG.${clr_end}\n" 1>&2
			usage
			exit 1
			;;
		:)
			printf "${clr_red}ERROR: Option -$OPTARG requires an argument.${clr_end}\n" 1>&2
			usage
			exit 1
			;;
	esac
done

thisScriptDir=$(realpath $(dirname "$0"))

if [ "$packageFormat" = pacman ] && [ ! -f /usr/bin/makepkg ]
then
    printf "${clr_yellow}WARNING: makepkg is missing. Pacman is most likely not the package manager of this system. The build will be delegated to Docker.${clr_end}\n"
    cd "$thisScriptDir/packaging/pacman"
    docker-compose build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) pacman_package
    docker-compose run pacman_package
    exit 0
fi

outDir="$thisScriptDir/dist/kmeldb-ui"
srcDir="$thisScriptDir/src"
if [ ! -d "$outDir" ]
then
	mkdir -p "$outDir"
else
	rm -r -f "$outDir/"*
fi

echo Copying files...
rsync -a --exclude=__pycache__/ "$srcDir/kmeldb_cli" "$outDir"
cp "$srcDir/aboutdialog.py" "$outDir"
cp "$srcDir/appresources_rc.py" "$outDir"
cp "$srcDir/driveutils.py" "$outDir"
cp "$srcDir/info.py" "$outDir"
cp "$srcDir/kenwooddbgen.png" "$outDir"
cp "$srcDir/kenwooddbgen.sh" "$outDir"
cp "$srcDir/mainwindow.py" "$outDir"
cp "$srcDir/preferencesdialog.py" "$outDir"
cp "$srcDir/program.py" "$outDir"
cp "$srcDir/settings.py" "$outDir"
cp "$srcDir/ui_"*.py "$outDir"
cp "$thisScriptDir/LICENSE" "$outDir"
mkdir "$outDir/translations" && cp "$srcDir/translations/"*.qm "$outDir/translations"
cp "$srcDir/requirements.txt" "$outDir"
cp "$thisScriptDir/packaging/create-venv.sh" "$outDir"

appVersion=$(python3 "$thisScriptDir/packaging/print_version.py")
packageMaintainer="Vladimir Svyatski <vsvyatski@yandex.ru>"
if [ "$packageFormat" = tgz ]
then
    echo Creating tar.gz archive...

    cd "$outDir"
    tar -czf "../kmeldb-ui_$appVersion.tar.gz" *
    cd -
    
    echo "Created archive $outDir/../kmeldb-ui_$appVersion.tar.gz"
elif [ "$packageFormat" = deb ]
then
    debTmpDir=$(mktemp -d)
    mkdir "$debTmpDir/opt" && cp -r "$outDir" "$debTmpDir/opt"
    mkdir -p "$debTmpDir/usr/share/applications/" && cp "$thisScriptDir/packaging/com.github.vsvyatski.kmeldb-ui.desktop" "$debTmpDir/usr/share/applications"

    packageDescription="Kenwood Music Editor Light replacement for Linux systems.
 This is a GUI application that can generate Kenwood DAP databases on a selected FAT32 formatted USB drive. The database is used by Kenwood car audio systems to allow searching by album, title, genre and artist. It also allows creation of playlists."

    cd "$debTmpDir"

    fpm -f -s dir -t deb -p "$outDir/../kmeldb-ui_${appVersion}_all.deb" -n kmeldb-ui -v ${appVersion} -m "$packageMaintainer" --category "utils" --deb-priority optional \
    --license GPL-3 --vendor "Vladimir Svyatski" -a all --url https://vsvyatski.github.io/kmeldb-ui --description "$packageDescription" --deb-installed-size 6342 \
    --deb-changelog "$thisScriptDir/packaging/deb/changelog" -d "python3-pyqt5 >= 5.5~" -d "python3-venv >= 3.5~" -d "python3-wheel >= 0.29~" --deb-recommends "qttranslations5-l10n >= 5.5~" \
    --after-install "$thisScriptDir/packaging/deb/postinst" --before-remove "$thisScriptDir/packaging/deb/prerm" .
    
    cd -
elif [ "$packageFormat" = pacman ]
then
    cd "$thisScriptDir/packaging/pacman"
    makepkg -f PACKAGER="$packageMaintainer" APPOUTDIR="$outDir" PROJROOTDIR="$thisScriptDir" APPVERSION="$appVersion" BUILDDIR="$thisScriptDir/out" PKGDEST="$thisScriptDir/dist"
    cd -
fi

echo Build has been successful.
