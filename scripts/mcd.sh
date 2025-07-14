#!/bin/bash
mcd () {
	mkdir -p "$1"
	cd "$1" || exit 1
}
#foobar
