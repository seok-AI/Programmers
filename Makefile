.PHONY: list navigation specs edge validate examples fuzz stress progress mock snippets new test

FUZZ_CASES ?= 500

list:
	python3 tools/judge.py --list

navigation:
	python3 tools/build_workspace.py --refresh-navigation

specs:
	python3 tools/offline_specs.py

edge:
	python3 tools/edge_case_bank.py

validate:
	python3 tools/validate.py

examples:
	python3 tools/check_example_solutions.py

fuzz:
	@if [ -n "$(PROBLEM)" ]; then \
		python3 tools/fuzz.py "$(PROBLEM)" --cases "$(FUZZ_CASES)"; \
	else \
		python3 tools/fuzz.py --all --oracles-only --cases "$(FUZZ_CASES)"; \
	fi

stress:
	python3 tools/stress.py --all

progress:
	python3 tools/progress.py --details

mock:
	python3 tools/mock.py start

snippets:
	python3 snippets/bfs.py
	python3 snippets/union_find.py
	python3 snippets/dijkstra.py

new:
	@if [ -z "$(SPEC)" ]; then \
		echo "사용법: make new SPEC=my_problem.json"; exit 2; \
	else \
		python3 tools/new_problem.py "$(SPEC)"; \
	fi

test:
	@if [ -n "$(PROBLEM)" ]; then \
		python3 tools/judge.py "$(PROBLEM)" && \
		python3 tools/fuzz.py "$(PROBLEM)" --cases "$(FUZZ_CASES)"; \
	else \
		python3 tools/judge.py --all; \
	fi
