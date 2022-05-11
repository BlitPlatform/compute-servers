#!/bin/bash

OPT_WORKDIR="`pwd`/build_debian"
OPT_REV='1'

OPTS=$(getopt \
	-o h,b:,r:,d:,k \
	-l help,branch:,revision:,work-dir:,keep,setup \
	-n "$0" \
	-- "$@") \
	|| exit
eval set -- "${OPTS}"
while [[ $1 != -- ]]
do
	case $1 in
		-h|--help) OPT_HELP='true' ; shift ;;
		-b|--branch) OPT_BRANCH="-b $2" ; shift 2 ;;
		-r|--revision) OPT_REV=$2 ; shift 2 ;;
		-d|--work-dir) OPT_WORKDIR=`realpath -s $2` ; shift 2 ;;
		-k|--keep) OPT_CLEAN='' ; shift ;;
		--setup) OPT_SETUP='true' ; shift ;;
		*) echo "Bad option: $1" >&2 ; exit 1 ;;
	esac
done
shift

_help () {
	echo "\
Usage:
	$0 [options]

Description:
	Build and install a recent .deb package of openems.

Options:
	-h, --help        Print this help.
	-b, --branch      Git commit hash of the 'thliebig/openEMS-Project' Github
	                  repository. Refer to the 'git-clone' manual for more infos.
	-r, --revision    Debian packaging revision number.
	-d, --work-dir    Working directory, defaults to './build_debian'.
	-k, --keep        Do not clean files after being done.
	--setup           Enable source APT repositories and install Debian
	                  packaging tools. Need to be done only once on a machine.
"
}

_setup () {
	sudo sed -Ei /etc/apt/sources.list -e 's/^# deb-src /deb-src /'
	sudo apt update
	sudo apt install -y devscripts
}

_build () {
	mkdir -p "${OPT_WORKDIR}"
	cd "${OPT_WORKDIR}"

	apt source --download-only openems
	git clone --recursive https://github.com/thliebig/openEMS-Project ${OPT_BRANCH}
	cd openEMS-Project

	VERSION="$(git describe --tags --abbrev=0 | cut -b 2-)+git$(git show -s --format=%cd.%h --date=format:'%Y%m%d')"

	tar -xvf ../openems_*.debian.tar.*
	sed -i debian/rules -e 's/-DCMAKE_BUILD_TYPE=Debug/-DCMAKE_BUILD_TYPE=Release/g'
	sed -i debian/changelog -e "1i \
openems (${VERSION}-${OPT_REV}) unstable; urgency=medium\n\n\
  * Package from upstream sources\n\n\
 -- Thomas Lepoix <thomas.lepoix@protonmail.ch>  $(date -R)\n\
"

	debuild -b -uc -us
}

_install () {
	cd "${OPT_WORKDIR}"
	sudo apt -y remove \
		libcsxcad0 \
		libnf2ff0 \
		libopenems0 \
		libqcsxcad0 \
		openems \
		octave-openems \
		python3-openems \
		openems-build-deps
	sudo apt -y install \
		./libcsxcad0_*.deb \
		./libnf2ff0_*.deb \
		./libopenems0_*.deb \
		./libqcsxcad0_*.deb \
		./openems_*.deb \
		./octave-openems_*.deb \
		./python3-openems_*.deb
}

_clean () {
	rm -rf "${OPT_WORKDIR}"
}

if [ "${OPT_HELP}" ]
then
	_help
elif [ "${OPT_SETUP}" ]
then
	_setup
else
	_clean
	_build
	_install
	[ "${OPT_CLEAN}" ] && _clean
fi

