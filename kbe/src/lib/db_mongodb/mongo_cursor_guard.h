#pragma once
#include <mongoc/mongoc.h>
#include <memory>

class MongoCursorGuard {
public:
    MongoCursorGuard(mongoc_collection_t* collection, mongoc_cursor_t* cursor)
        : collection_(collection), cursor_(cursor) {
    }

    MongoCursorGuard(const MongoCursorGuard&) = delete;
    MongoCursorGuard& operator=(const MongoCursorGuard&) = delete;

    MongoCursorGuard(MongoCursorGuard&& other) noexcept
        : collection_(other.collection_), cursor_(other.cursor_) {
        other.collection_ = nullptr;
        other.cursor_ = nullptr;
    }

    MongoCursorGuard& operator=(MongoCursorGuard&& other) noexcept {
        if (this != &other) {
            destroy();
            collection_ = other.collection_;
            cursor_ = other.cursor_;
            other.collection_ = nullptr;
            other.cursor_ = nullptr;
        }
        return *this;
    }

    ~MongoCursorGuard() {
        destroy();
    }

    mongoc_collection_t* collection() const { return collection_; }
    mongoc_cursor_t* cursor() const { return cursor_; }

private:
    void destroy() {
        if (cursor_) {
            mongoc_cursor_destroy(cursor_);
            cursor_ = nullptr;
        }
        if (collection_) {
            mongoc_collection_destroy(collection_);
            collection_ = nullptr;
        }
    }

    mongoc_collection_t* collection_ = nullptr;
    mongoc_cursor_t* cursor_ = nullptr;
};