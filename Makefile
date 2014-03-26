.PHONY: modules

modules:
	git submodule update --init --remote --rebase --recursive
