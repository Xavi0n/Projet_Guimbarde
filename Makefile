# === CONFIGURATION ===
CC = gcc
CFLAGS = -Wall -Isrc $(shell python3-config --includes)
LDFLAGS = $(shell python3-config --ldflags)

SRC_DIR = src
OBJ_DIR = build
BIN = main

SRC = $(wildcard $(SRC_DIR)/*.c)
OBJ = $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# === RULES ===

all: $(BIN) python_check

$(BIN): $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $@

python_check:
	@echo "Checking Python scripts..."
	@python -c "import py_compile; py_compile.compile('py files/HuskyLens_ReadAndParse.py')"

clean:
	rm -rf $(OBJ_DIR) $(BIN)
	rm -f py files/*.pyc

.PHONY: all clean python_check
