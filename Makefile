.PHONY: all clean install

SHELL=/bin/bash
 
DAYS := $(shell ls */[0-9][0-9]/input.txt | sed -e 's:/input.txt::')
OUTPUTS := $(DAYS:%=%/output.txt)

all: $(OUTPUTS) $(OUTPUTS_MOD) check.txt
install: .venv-pypy3/installed .venv-python3/installed
clean:
	rm -fR */*/output.txt check.txt .venv*

.venv-pypy3/installed: requirements.txt
	pypy3 -m venv .venv-pypy3
	.venv-pypy3/bin/pip install -r requirements.txt
	touch .venv-pypy3/installed

.venv-python3/installed: requirements.txt
	python3 -m venv .venv-python3
	.venv-python3/bin/pip install -r requirements.txt
	touch .venv-python3/installed

define DAYRULE
$D/output.txt: $D/*.py $D/input*.txt .venv-python3/bin/activate .venv-pypy3/bin/activate
	./run.sh $D
endef

$(foreach D,$(DAYS),$(eval $(DAYRULE)))

check.txt: $(OUTPUTS) $(shell ls */*/answers.txt) check.sh
	yes | ./check.sh > check.txt
