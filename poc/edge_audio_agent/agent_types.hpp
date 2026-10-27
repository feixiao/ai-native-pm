#pragma once
#include <string>
#include <vector>
#include <chrono>
#include <cstdint>

namespace edge_agent {

// 4音区定义
enum class AudioZone : uint8_t {
    Driver = 0,      // 主驾 (Zone 0)
    CoDriver = 1,    // 副驾 (Zone 1)
    RearLeft = 2,    // 左后 (Zone 2)
    RearRight = 3    // 右后 (Zone 3)
};

inline const char* zoneToString(AudioZone zone) {
    switch (zone) {
        case AudioZone::Driver: return "Driver (Zone 0)";
        case AudioZone::CoDriver: return "CoDriver (Zone 1)";
        case AudioZone::RearLeft: return "RearLeft (Zone 2)";
        case AudioZone::RearRight: return "RearRight (Zone 3)";
        default: return "Unknown";
    }
}

// 指令优先级与安全域
enum class IntentDomain : uint8_t {
    SafetyCritical = 0, // P0: 绝对安全/阻断类
    FastVehicleControl, // P0: 0算力硬车控 (空调/车窗/座椅)
    PersonalizedMemory, // P1: 记忆查询与偏好应用
    GeneralChat,        // P2: 通用对话 / 闲聊
    SafetyBlocked       // 拒绝执行 (权限不足或安全违规)
};

// 提取的槽位实体
struct SlotEntity {
    std::string key;
    std::string value;
};

// 解析决策结果
struct DispatchResult {
    IntentDomain domain;
    AudioZone zone;
    std::string targetAction; // 如 "SET_AC_TEMP", "OPEN_WINDOW", "SET_MEMORY"
    std::vector<SlotEntity> slots;
    std::string ttsResponse;
    bool executeCAN;
    double routingLatencyUs;  // 路由判定耗时 (微秒)
};

// 本地记忆条目
struct MemoryItem {
    std::string profileId;
    std::string key;
    std::string value;
    float confidence;
    int triggerCount;
};

} // namespace edge_agent
