#!/bin/bash

# Import Settings
. settings

if [ ! -f "./VMImages/loader-lucid-amd64-linux-image-2.6.32-34-virtual-v-2.6.32-34.77~smloader0-build0.tar.gz" ] ; then
	echo "Downloading loader"
	wget http://people.canonical.com/~smoser/lucid-loaders/loader-lucid-amd64-linux-image-2.6.32-34-virtual-v-2.6.32-34.77~smloader0-build0.tar.gz
fi

if [ ! -f "./VMImages/loader-ramdisks.txt" ] ; then
	echo "Extracting loader"
	tar xfzv ./VMImages/loader-lucid-amd64-linux-image-2.6.32-34-virtual-v-2.6.32-34.77~smloader0-build0.tar.gz -C ./VMImages
fi

TOKEN=`./obtain-token.sh`

echo "Uploading loader kernel"
RVAL=`glance -A $TOKEN add name="loader-kernel" is_public=true container_format=aki disk_format=aki < ./VMImages/kernels/lucid-amd64-linux-image-2.6.32-34-virtual-v-2.6.32-34.77~smloader0-kernel`
KERNEL_ID=`echo $RVAL | cut -d":" -f2 | tr -d " "`

echo "Uploading loader ramdisk"
RVAL=`glance -A $TOKEN add name="loader-ramdisk" is_public=true container_format=ari disk_format=ari < ./VMImages/loader-ramdisks/lucid-amd64-linux-image-2.6.32-34-virtual-v-2.6.32-34.77~smloader0-build0-loader`
RAMDISK_ID=`echo $RVAL | cut -d":" -f2 | tr -d " "`

