.PHONY: all clean

SHELL=/bin/bash
 
DAYS := $(shell ls */[0-9][0-9]/input.txt | sed -e 's:/input.txt::')
OUTPUTS := $(DAYS:%=%/output.txt)

all: $(OUTPUTS) $(OUTPUTS_MOD) check.txt
clean:
	rm -f */*/output.txt check.txt

define DAYRULE
$D/output.txt: $D/*.py $D/input*.txt
	cd $D; \
	if [ -e input-mod.txt ]; then \
	  ./p.py 1 < input.txt > output.txt; \
	  ./p.py 2 < input-mod.txt >> output.txt; \
	else \
	  ./p.py 1 2 < input.txt > output.txt; \
	fi; \
	cd ../..
endef

$(foreach D,$(DAYS),$(eval $(DAYRULE)))

check.txt: $(OUTPUTS) $(shell ls */*/answers.txt) check.sh
	yes | ./check.sh > check.txt
