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
    echo '    supported formats:'
    echo "      tgz - a *.tar.gz archive, it's distribution independent, but requires"
    echo '            manual installation'
    echo '      deb - a *.deb package for Debian and derivatives'
    echo '  -v <version_number>  add version number to the archive name (used with -p)'
}

checkFormat() {
    local format=$1
    test ${format} = tgz -o ${format} = deb
}

while getopts ":p:hv:" opt; do
	case ${opt} in
	    h)
	        usage
	        exit
	        ;;
		p)
			package_format=$OPTARG
			if ! checkFormat $package_format
			then
                printf "${clr_red}ERROR: Unrecognized target package format \"$package_format\"${clr_end}\n" 1>&2
                usage
                exit 1
			fi
			;;
		v)
			version_suffix="-$OPTARG"
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

currentDir=$(dirname "$0")

outDir="$currentDir/dist/kmeldb-ui"
srcDir="$currentDir/src"
if [ ! -d "$outDir" ]
then
	mkdir -p "$outDir"
else
	rm -r -f "$outDir/"*
fi

echo Copying files...
cp -r "$srcDir/kmeldb_cli" "$outDir"
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
cp "$currentDir/LICENSE" "$outDir"
mkdir "$outDir/translations" && cp "$srcDir/translations/"*.qm "$outDir/translations"

echo Generating virtual environment...
python3 -m venv --system-site-packages "$outDir/venv"
"$outDir/venv/bin/pip3" install -r "$srcDir/requirements.txt"

if [ ${package_format} = tgz ]
then
    echo Creating tar.gz archive...

    cd "$outDir"
    tar -czf "../kmeldb-ui$version_suffix.tar.gz" *
    cd -
elif [ ${package_format} = deb ]
then
    fpm -s dir -t deb -p "$outDir/../kmeldb-ui$version_suffix.deb" -n kmeldb-ui -v 0.3.0 -m "Vladimir Svyatski <vsvyatski@yandex.ru>" --category "utils" --license GPL-3 --vendor "Vladimir Svyatski" "$outDir"
fi

echo Build has been successful.
