.PHONY: all install clean realclean check measure

SHELL=/bin/bash
 
DAYS := $(shell ls */[0-9][0-9]/input.txt | sed -e 's:/input.txt::')
OUTPUTS := $(DAYS:%=%/output.txt)

all: ../aoc-input $(OUTPUTS) $(OUTPUTS_MOD) check.txt
install: .venv-pypy3/installed .venv-python3/installed .nim ../aoc-input
clean:
	rm -fR */*/output.txt check.txt
realclean:
	rm -fR */*/output.txt check.txt .venv-* .nim
check:
	make clean && time make -s -j$(shell nproc) all && git status
measure:
	make clean && time make -s all | sort -k2n && git status

.venv-pypy3/installed: requirements.txt
	pypy3 -m venv .venv-pypy3
	.venv-pypy3/bin/pip install -r requirements.txt
	touch .venv-pypy3/installed

.venv-python3/installed: requirements.txt
	python3 -m venv .venv-python3
	.venv-python3/bin/pip install -r requirements.txt
	touch .venv-python3/installed

.nim:
	if [ "$$(uname)" == "Darwin" ]; then brew install nim && mkdir .nim; else wget https://nim-lang.org/download/nim-2.2.6-linux_x64.tar.xz && tar Jxf nim-*.tar.xz && mv nim-2.2.6 .nim && rm nim-*.tar.xz && .nim/bin/nimble install itertools; fi

../aoc-input:
	git clone git@github.com:mattbillenstein/aoc-input.git ../aoc-input

define DAYRULE
$D/output.txt: $D/*.py $D/input*.txt .venv-python3/installed .venv-pypy3/installed
	./run.sh $D
endef

$(foreach D,$(DAYS),$(eval $(DAYRULE)))

check.txt: $(OUTPUTS) $(shell ls */*/answers.txt) check.sh
	yes | ./check.sh > check.txt
