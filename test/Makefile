.PHONY: all

all: venv/lib/libhidapi-libusb.so venv

venv: requirements.txt
	[ -d $@ ] || virtualenv -p $(shell which python2.7) $@
	$@/bin/pip install -r $<
	touch $@

venv/src: venv
	mkdir -p $@

venv/src/hidapi-0.7.0.zip: venv/src
	sha256sum -c sha256sum.txt || curl https://cloud.github.com/downloads/signal11/hidapi/hidapi-0.7.0.zip > $@

venv/src/hidapi-0.7.0: venv/src/hidapi-0.7.0.zip
	rm -rf $@
	unzip $< -d $(dir $@)
	touch $@

venv/src/hidapi-0.7.0/linux/hid.o: venv/src/hidapi-0.7.0
	CFLAGS="-I../hidapi -Wall -g -c -fPIC" make -C $</linux $(notdir $@)

venv/src/hidapi-0.7.0/linux/hid-libusb.o: venv/src/hidapi-0.7.0
	CFLAGS="-fPIC" make -C $</linux $(notdir $@)

venv/lib/libhidapi-libusb.so: venv/src/hidapi-0.7.0/linux/hid-libusb.o
	gcc -shared -o $@ $<

clean:
	rm -rf venv
