.PHONY: all clean

SHELL=/bin/bash
 
DAYS := $(shell ls */[0-9][0-9]/input.txt | sed -e 's:/input.txt::')
OUTPUTS := $(DAYS:%=%/output.txt)

all: $(OUTPUTS) $(OUTPUTS_MOD) check.txt
clean:
	rm -f */*/output.txt check.txt

define DAYRULE
$D/output.txt: $D/*.py $D/input*.txt
	./run.sh $D
endef

$(foreach D,$(DAYS),$(eval $(DAYRULE)))

check.txt: $(OUTPUTS) $(shell ls */*/answers.txt) check.sh
	yes | ./check.sh > check.txt
