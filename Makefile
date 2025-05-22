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

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $@

clean:
	rm -rf $(OBJ_DIR) $(BIN)

.PHONY: all clean
