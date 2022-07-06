#!/bin/bash

OPT_WORKDIR="`pwd`/build_debian"
OPT_URL='https://github.com/thliebig/openEMS-Project'
OPT_REV='1'
OPT_ENGINE='fastest'

OPTS=$(getopt \
	-o h,u:,b:,r:,d:,k \
	-l help,url:,branch:,revision:,work-dir:,keep,benchmark,engine,setup \
	-n "$0" \
	-- "$@") \
	|| exit
eval set -- "${OPTS}"
while [[ $1 != -- ]]
do
	case $1 in
		-h|--help) OPT_HELP='true' ; shift ;;
		-u|--url) OPT_URL=$2 ; shift 2 ;;
		-b|--branch) OPT_BRANCH="-b $2" ; shift 2 ;;
		-r|--revision) OPT_REV=$2 ; shift 2 ;;
		-d|--work-dir) OPT_WORKDIR=`realpath -s $2` ; shift 2 ;;
		-k|--keep) OPT_CLEAN='' ; shift ;;
		--benchmark) OPT_BENCHMARK='true' ; shift ;;
		-e|--engine) OPT_ENGINE=$3 ; shift ;;
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
	-u, --url         Alternative git repository url. Should only be a fork of
	                  the 'thliebig/openEMS-Project' GitHub repository that is
	                  the default.
	-b, --branch      Git commit hash of the git repository. Refer to the
	                  'git-clone' manual for more infos.
	-r, --revision    Debian packaging revision number.
	-d, --work-dir    Working directory, defaults to './build_debian'.
	-k, --keep        Do not clean files after being done.
	--setup           Enable source APT repositories and install Debian
	                  packaging tools. Need to be done only once on a machine.
	--benchmark       Run benchmark on a test case to evaluate solver performance.
	-e, --engine      Engine to benchmark (fastest/basic/sse/sse-compressed/multithreaded).
"
}

_benchmark () {
	killall openEMS 2>/dev/null
	rm -rf benchmark_tmp
	mkdir benchmark_tmp
	cd benchmark_tmp
	wget https://raw.githubusercontent.com/BlitPlatform/compute-servers/main/benchmark.xml 2>/dev/null
	echo "============================================"
	echo "Running benchmark (this will take 20 sec)..."
	openEMS benchmark.xml --engine="${OPT_ENGINE}" > benchmark.txt & (sleep 20; killall openEMS)
	echo "Benchmark complete."
	echo "============================================"
	cat benchmark.txt | grep -o -z -P '(?<=enabled ).*\n'
	echo "============================================"
	cat benchmark.txt | grep -o -P '(?<=\|\| ).*(?= \|\|)'
	echo "============================================"
	rm -rf *
	cd ..
	rm -rf benchmark_tmp
}

_setup () {
	sudo sed -Ei /etc/apt/sources.list -e 's/^# deb-src /deb-src /'
	sudo apt update
	sudo apt install -y git python3-setuptools python3-pip devscripts equivs
}

_build () {
	mkdir -p "${OPT_WORKDIR}"
	cd "${OPT_WORKDIR}"

	apt source --download-only openems
	git clone --recursive --remote-submodules ${OPT_URL} ${OPT_BRANCH}
	cd openEMS-Project

	VERSION="$(git describe --tags --abbrev=0 | cut -b 2-)+git$(git show -s --format=%cd.%h --date=format:'%Y%m%d')"

	tar -xvf ../openems_*.debian.tar.*
	sed -i debian/rules -e 's/-DCMAKE_BUILD_TYPE=Debug/-DCMAKE_BUILD_TYPE=Release/g'
	sed -i debian/changelog -e "1i \
openems (${VERSION}-${OPT_REV}) unstable; urgency=medium\n\n\
  * Package from upstream sources\n\n\
 -- Thomas Lepoix <thomas.lepoix@protonmail.ch>  $(date -R)\n\
"

	sudo mk-build-deps -i
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
elif [ "${OPT_BENCHMARK}" ]
then
	_benchmark
elif [ "${OPT_SETUP}" ]
then
	_setup
else
	_clean
	_build
	_install
	[ "${OPT_CLEAN}" ] && _clean
fi
