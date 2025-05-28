# === CONFIGURATION ===
CC = gcc
CFLAGS = -Wall -Isrc $(shell python3-config --includes)
LDFLAGS = $(shell python3-config --ldflags)

SRC_DIR = src
OBJ_DIR = build
BIN = main
TEST_BIN = test_huskylens

SRC = $(wildcard $(SRC_DIR)/*.c)
OBJ = $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Test-specific source and object files
TEST_SRC = $(SRC_DIR)/test_huskylens.c $(SRC_DIR)/huskylens_api.c
TEST_OBJ = $(TEST_SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# === RULES ===

all: $(BIN) python_check

test: $(TEST_BIN)

$(BIN): $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

$(TEST_BIN): $(TEST_OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $@

python_check:
	@echo "Checking Python scripts..."
	@python -c "import py_compile; py_compile.compile('py files/HuskyLens_ReadAndParse.py')"

clean:
	rm -rf $(OBJ_DIR) $(BIN) $(TEST_BIN)
	rm -f py files/*.pyc

.PHONY: all clean python_check test
