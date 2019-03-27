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

thisScriptDir=$(dirname "$0")

# First of all we need to build the distribution
echo Started application build.
echo
sh "$thisScriptDir/build.sh"
if [ $? != 0 ]
then
    printf "${clr_red}ERROR: Distribution build failed, stopping PPA publishing.${clr_end}\n" 1>&2
    exit 1
fi
echo
echo Finished application build.

outDir="$thisScriptDir/out/ppa"
packageVersion=$(python3 "$thisScriptDir/packaging/print_version.py")
packageSrcDir="$outDir/kmeldb-ui_$packageVersion"
if [ ! -d "$packageSrcDir" ]
then
	mkdir -p "$packageSrcDir"
else
	rm -r -f "$packageSrcDir/"*
fi

echo Preparing source package...
cp -r "$thisScriptDir/packaging/deb/unstable/debian" "$packageSrcDir"
cp "$thisScriptDir/packaging/deb/unstable/Makefile" "$packageSrcDir"
# Let's copy the distribution files
cp -r "$thisScriptDir/dist/kmeldb-ui" "$packageSrcDir"
cp "$thisScriptDir/packaging/com.github.vsvyatski.kmeldb-ui.desktop" "$packageSrcDir"
