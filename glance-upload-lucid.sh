#!/bin/bash

# Import Settings
. settings

echo "Use glance-upload-loader.sh followed by glance-upload-lucid-loader.sh instead"

exit 1

if [ ! -f "./VMImages/lucid-server-cloudimg-amd64.tar.gz" ] ; then
	echo "Downloading image"
	wget http://cloud-images.ubuntu.com/lucid/current/lucid-server-cloudimg-amd64.tar.gz
fi

if [ ! -f "./VMImages/lucid-server-cloudimg-amd64.img" ] ; then
        echo "Extracting image"
	tar xfzv ./VMImages/lucid-server-cloudimg-amd64.tar.gz -C ./VMImages
fi

TOKEN=`./obtain-token.sh`
echo "Uploading kernel"
RVAL=`glance -A $TOKEN add name="ubuntu-lucid-kernel" is_public=true container_format=aki disk_format=aki < ./VMImages/lucid-server-cloudimg-amd64-vmlinuz-virtual`
KERNEL_ID=`echo $RVAL | cut -d":" -f2 | tr -d " "`

echo "Uploading image"
glance -A $TOKEN add name="ubuntu-lucid" is_public=true container_format=ami kernel_id=$KERNEL_ID disk_format=ami < ./VMImages/lucid-server-cloudimg-amd64.img
