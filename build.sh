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
	clr_end=$'\e[0m'
else
	clr_red=''
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
                printf "${clr_red}ERROR: Unrecognized target package format \"$packageFormat\"${clr_end}\n" 1>&2
                usage
                exit 1
			fi
			;;
		\?)
			printf "${clr_red}ERROR: Unrecognized option -$OPTARG${clr_end}\n" 1>&2
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
cp "$thisScriptDir/packaging/install-venv.sh" "$outDir"

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
    --license GPL-3 --vendor "Vladimir Svyatski" -a all --url https://github.com/vsvyatski/kmel_db_ui --description "$packageDescription" --deb-installed-size 6342 \
    --deb-changelog "$thisScriptDir/packaging/deb/debian/changelog" -d "python3-pyqt5 >= 5.5~" -d "python3-venv >= 3.5~" -d "python3-wheel >= 0.29~" --deb-recommends "qttranslations5-l10n >= 5.5~" \
    --after-install "$thisScriptDir/packaging/deb/debian/postinst" --before-remove "$thisScriptDir/packaging/deb/debian/prerm" .
    
    cd -
elif [ "$packageFormat" = pacman ]
then
    # NOTE: fpm currently has a bug with --pacman-optional-depends, therefore makepkg is used.

#     pacmanTmpDir=$(mktemp -d)
#     mkdir "$pacmanTmpDir/opt" && cp -r "$outDir" "$pacmanTmpDir/opt"
#     mkdir -p "$pacmanTmpDir/usr/share/applications/" && cp "$thisScriptDir/packaging/com.github.vsvyatski.kmeldb-ui.desktop" "$pacmanTmpDir/usr/share/applications"
#     
#     packageDescription="Kenwood Music Editor Light replacement for Linux systems"
#     # Let's define this explicitely, it seems to be important for Pacman (otherwise fpm will implicitely set this to 1)
#     iteration=1
# 
#     cd "$pacmanTmpDir"
# 
#     fpm -f -s dir -t pacman -p "$outDir/../kmeldb-ui-${appVersion}-${iteration}-any.pkg.tar.xz" -n kmeldb-ui -v ${appVersion} -m "$packageMaintainer" \
#     --license GPL3 -a all --url https://github.com/vsvyatski/kmel_db_ui --description "$packageDescription" --iteration $iteration \
#     -d python-pyqt5 --pacman-optional-depends qt5-translations \
#     --after-install "$thisScriptDir/packaging/after-install.sh" --after-remove "$thisScriptDir/packaging/after-remove.sh" .
#     
#     cd -

    cd "$thisScriptDir/packaging/pacman"
    makepkg -f PACKAGER="$packageMaintainer" APPOUTDIR="$outDir" PROJROOTDIR="$thisScriptDir" APPVERSION="$appVersion" BUILDDIR="$thisScriptDir/out" PKGDEST="$thisScriptDir/dist"
    cd -
fi

echo Build has been successful.
