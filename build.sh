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
    echo '  -p                   pack build results into tar.gz archive'
    echo '  -v <version_number>  add version number to the archive name (used with -p)'
}

pack=false

while getopts ":phv:" opt; do
	case ${opt} in
	    h)
	        usage
	        exit
	        ;;
		p)
			pack=true
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
cp "$srcDir/program.py" "$outDir"
cp "$srcDir/settings.py" "$outDir"
cp "$srcDir/ui_"*.py "$outDir"
cp "$currentDir/LICENSE" "$outDir"

echo Generating virtual environment...
python3 -m venv --system-site-packages "$outDir/venv"

if [ ${pack} = true ]
then
    echo Packing...

    cd "$outDir"
    tar -czf "../kmeldb-ui$version_suffix.tar.gz" *
    cd -
fi

echo Build has been successful.
