#pragma once
#include "agent_types.hpp"
#include <sqlite3.h>
#include <iostream>
#include <memory>
#include <mutex>
#include <unordered_map>
#include <fstream>
#include <sstream>

namespace edge_agent {

class LocalMemoryEngine {
public:
    LocalMemoryEngine(const std::string& dbPath) : dbPath_(dbPath), db_(nullptr) {}

    ~LocalMemoryEngine() {
        close();
    }

    bool init() {
        std::lock_guard<std::mutex> lock(mtx_);
        // 打开端侧 SQLite 数据库
        int rc = sqlite3_open(dbPath_.c_str(), &db_);
        if (rc != SQLITE_OK) {
            std::cerr << "[MemoryEngine] Failed to open DB: " << sqlite3_errmsg(db_) << std::endl;
            return false;
        }

        // 启用 WAL 模式降低写入阻塞并延长存储寿命
        char* errMsg = nullptr;
        sqlite3_exec(db_, "PRAGMA journal_mode=WAL;", nullptr, nullptr, &errMsg);
        sqlite3_exec(db_, "PRAGMA synchronous=NORMAL;", nullptr, nullptr, &errMsg);

        // 创建本地偏好记忆表
        const char* createSql = 
            "CREATE TABLE IF NOT EXISTS local_user_memory ("
            "  profile_id TEXT NOT NULL,"
            "  memory_key TEXT NOT NULL,"
            "  memory_val TEXT NOT NULL,"
            "  confidence REAL DEFAULT 1.0,"
            "  trigger_count INT DEFAULT 1,"
            "  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  PRIMARY KEY (profile_id, memory_key)"
            ");";

        rc = sqlite3_exec(db_, createSql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::cerr << "[MemoryEngine] Table creation failed: " << errMsg << std::endl;
            sqlite3_free(errMsg);
            return false;
        }

        // 预热内存缓存 (In-Memory Hot Cache) 避免车控时发生物理 IO
        loadCacheFromDB();
        return true;
    }

    // 内存极速查找 (0 IO, < 100微秒)
    bool getMemoryFast(const std::string& profileId, const std::string& key, std::string& outVal) {
        std::lock_guard<std::mutex> lock(mtx_);
        std::string cacheKey = profileId + "#" + key;
        auto it = memoryCache_.find(cacheKey);
        if (it != memoryCache_.end()) {
            outVal = it->second;
            return true;
        }
        return false;
    }

    // 写入记忆 (写入内存缓存 + 异步/延迟落盘)
    bool putMemory(const std::string& profileId, const std::string& key, const std::string& val, float confidence = 1.0f) {
        std::lock_guard<std::mutex> lock(mtx_);
        std::string cacheKey = profileId + "#" + key;
        memoryCache_[cacheKey] = val;

        if (!db_) return false;

        const char* upsertSql = 
            "INSERT INTO local_user_memory (profile_id, memory_key, memory_val, confidence, trigger_count, last_updated) "
            "VALUES (?, ?, ?, ?, 1, CURRENT_TIMESTAMP) "
            "ON CONFLICT(profile_id, memory_key) DO UPDATE SET "
            "  memory_val = excluded.memory_val, "
            "  confidence = excluded.confidence, "
            "  trigger_count = trigger_count + 1, "
            "  last_updated = CURRENT_TIMESTAMP;";

        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(db_, upsertSql, -1, &stmt, nullptr) != SQLITE_OK) {
            return false;
        }

        sqlite3_bind_text(stmt, 1, profileId.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, key.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, val.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_double(stmt, 4, confidence);

        int rc = sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        return rc == SQLITE_DONE;
    }

    void close() {
        std::lock_guard<std::mutex> lock(mtx_);
        if (db_) {
            sqlite3_close(db_);
            db_ = nullptr;
        }
    }

private:
    void loadCacheFromDB() {
        if (!db_) return;
        const char* query = "SELECT profile_id, memory_key, memory_val FROM local_user_memory;";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(db_, query, -1, &stmt, nullptr) == SQLITE_OK) {
            while (sqlite3_step(stmt) == SQLITE_ROW) {
                std::string pid = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
                std::string k = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
                std::string v = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
                memoryCache_[pid + "#" + k] = v;
            }
            sqlite3_finalize(stmt);
        }
    }

    std::string dbPath_;
    sqlite3* db_;
    std::mutex mtx_;
    std::unordered_map<std::string, std::string> memoryCache_;
};

} // namespace edge_agent
