#!/bin/bash

sudo cp /etc/apt/sources.list /etc/apt/sources.list~
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
sudo apt -y update

apt source openems
sudo apt -y build-dep ./openems*.dsc
sudo apt -y install devscripts

cd openems*/
sed -e 's/-DCMAKE_BUILD_TYPE=Debug/-DCMAKE_BUILD_TYPE=Release/g' -i debian/rules
debuild -b -uc -us

cd ..
sudo apt -y remove libcsxcad0 libnf2ff0 libopenems0 libqcsxcad0 openems octave-openems
sudo apt -y install ./libcsxcad0*.deb ./libnf2ff0*.deb ./libopenems0*.deb ./libqcsxcad0*.deb ./openems*.deb ./octave-openems*.deb ./python3-openems*.deb
