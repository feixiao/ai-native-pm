#pragma once
#include "agent_types.hpp"
#include "local_memory_engine.hpp"
#include <regex>
#include <chrono>
#include <sstream>

namespace edge_agent {

class FastSlotRouter {
public:
    FastSlotRouter(std::shared_ptr<LocalMemoryEngine> memory) 
        : memory_(memory) {}

    DispatchResult process(AudioZone zone, const std::string& transcript, const std::string& currentProfileId = "driver_default") {
        auto start = std::chrono::high_resolution_clock::now();
        DispatchResult res;
        res.zone = zone;
        res.executeCAN = false;

        // 1. P0 级绝对安全与合规拦截 (Safety Boundary)
        if (checkSafetyViolations(transcript, res)) {
            auto end = std::chrono::high_resolution_clock::now();
            res.routingLatencyUs = std::chrono::duration<double, std::micro>(end - start).count();
            return res;
        }

        // 2. 权限隔离校验 (后排试图控制整车级安全动作)
        if (checkZonePrivilege(zone, transcript, res)) {
            auto end = std::chrono::high_resolution_clock::now();
            res.routingLatencyUs = std::chrono::duration<double, std::micro>(end - start).count();
            return res;
        }

        // 3. 记忆显式学习匹配 (如: "记住我老婆坐副驾喜欢26度" / "记一下...")
        if (handleExplicitMemoryCommand(transcript, currentProfileId, res)) {
            auto end = std::chrono::high_resolution_clock::now();
            res.routingLatencyUs = std::chrono::duration<double, std::micro>(end - start).count();
            return res;
        }

        // 4. 结合个性化记忆的极速车控 (如: "我老婆上车了" 或 "开到我习惯的温度")
        if (handlePersonalizedControl(transcript, zone, currentProfileId, res)) {
            auto end = std::chrono::high_resolution_clock::now();
            res.routingLatencyUs = std::chrono::duration<double, std::micro>(end - start).count();
            return res;
        }

        // 5. 0 算力依赖的常规本地车控 (空调、车窗等正则槽位快速命中)
        if (handleDirectVehicleControl(transcript, zone, res)) {
            auto end = std::chrono::high_resolution_clock::now();
            res.routingLatencyUs = std::chrono::duration<double, std::micro>(end - start).count();
            return res;
        }

        // 6. 兜底分流至端侧本地小模型 SLM (或可选云端)
        res.domain = IntentDomain::GeneralChat;
        res.targetAction = "FALLBACK_EDGE_SLM";
        res.ttsResponse = "正在为您思考中...";
        auto end = std::chrono::high_resolution_clock::now();
        res.routingLatencyUs = std::chrono::duration<double, std::micro>(end - start).count();
        return res;
    }

private:
    bool checkSafetyViolations(const std::string& text, DispatchResult& res) {
        // 严禁大模型触碰动力/底盘/刹车安全
        static const std::regex kSafetyRegex("刹车|急刹|熄火|漂移|追尾|转向断开|关闭大灯");
        if (std::regex_search(text, kSafetyRegex)) {
            res.domain = IntentDomain::SafetyCritical;
            res.targetAction = "REJECT_SAFETY_VIOLATION";
            res.ttsResponse = "安全提示：该操作涉及行车安全，语音助手已被硬件级阻断。";
            res.executeCAN = false;
            return true;
        }
        return false;
    }

    bool checkZonePrivilege(AudioZone zone, const std::string& text, DispatchResult& res) {
        // 后排不能私自修改驾驶模式、开关儿童锁等整车独占功能
        static const std::regex kDriverOnlyRegex("驾驶模式|运动模式|经济模式|儿童锁|打开后备箱");
        if (zone != AudioZone::Driver && std::regex_search(text, kDriverOnlyRegex)) {
            res.domain = IntentDomain::SafetyBlocked;
            res.targetAction = "REJECT_UNAUTHORIZED_ZONE";
            res.ttsResponse = "抱歉，该功能仅支持主驾驶员操作。";
            res.executeCAN = false;
            return true;
        }
        return false;
    }

    bool handleExplicitMemoryCommand(const std::string& text, const std::string& profileId, DispatchResult& res) {
        // 匹配："记住/记一下 [实体] 喜欢/习惯 [参数]"
        static const std::regex kMemoryPattern("(?:记住|记一下).*?(老婆|副驾|女儿).*?([0-9]{2})度");
        std::smatch match;
        if (std::regex_search(text, match, kMemoryPattern)) {
            std::string person = match[1].str();
            std::string temp = match[2].str();

            std::string key = (person == "老婆" || person == "副驾") ? "wife_ac_temp" : "daughter_ac_temp";
            memory_->putMemory(profileId, key, temp);

            res.domain = IntentDomain::PersonalizedMemory;
            res.targetAction = "SAVE_PREFERENCE";
            res.slots.push_back({"target_person", person});
            res.slots.push_back({"temp", temp});
            res.ttsResponse = "好的，已在本地记住：" + person + "习惯温度为 " + temp + " 度。";
            res.executeCAN = false;
            return true;
        }
        return false;
    }

    bool handlePersonalizedControl(const std::string& text, AudioZone zone, const std::string& profileId, DispatchResult& res) {
        // 场景 1: "我老婆上车了" -> 自动应用副驾偏好
        if (text.find("老婆上车") != std::string::npos || text.find("小丽上车") != std::string::npos) {
            std::string savedTemp;
            if (memory_->getMemoryFast(profileId, "wife_ac_temp", savedTemp)) {
                res.domain = IntentDomain::FastVehicleControl;
                res.targetAction = "SET_AC_TEMP";
                res.slots.push_back({"target_zone", "Zone 1 (副驾)"});
                res.slots.push_back({"temp", savedTemp});
                res.ttsResponse = "欢迎副驾，已根据本地记忆将副驾空调自动调节至 " + savedTemp + " 度。";
                res.executeCAN = true;
                return true;
            }
        }

        // 场景 2: "按我的习惯开空调"
        if (text.find("习惯") != std::string::npos && text.find("空调") != std::string::npos) {
            std::string savedTemp;
            if (memory_->getMemoryFast(profileId, "wife_ac_temp", savedTemp)) {
                res.domain = IntentDomain::FastVehicleControl;
                res.targetAction = "SET_AC_TEMP";
                res.slots.push_back({"target_zone", zoneToString(zone)});
                res.slots.push_back({"temp", savedTemp});
                res.ttsResponse = "已按本地专属记忆将空调调至 " + savedTemp + " 度。";
                res.executeCAN = true;
                return true;
            }
        }
        return false;
    }

    bool handleDirectVehicleControl(const std::string& text, AudioZone zone, DispatchResult& res) {
        // 空调温度: "把空调调到24度" / "温度设为25度"
        static const std::regex kAcTempRegex("(?:空调|温度).*?([1-3][0-9])度");
        std::smatch match;
        if (std::regex_search(text, match, kAcTempRegex)) {
            std::string temp = match[1].str();
            res.domain = IntentDomain::FastVehicleControl;
            res.targetAction = "SET_AC_TEMP";
            res.slots.push_back({"zone", zoneToString(zone)});
            res.slots.push_back({"temp", temp});
            res.ttsResponse = std::string(zoneToString(zone)) + " 空调已设定为 " + temp + " 度。";
            res.executeCAN = true;
            return true;
        }

        // 车窗控制: "把车窗打开一半" / "打开车窗"
        if (text.find("车窗") != std::string::npos) {
            res.domain = IntentDomain::FastVehicleControl;
            res.targetAction = (text.find("关") != std::string::npos) ? "CLOSE_WINDOW" : "OPEN_WINDOW";
            res.slots.push_back({"zone", zoneToString(zone)});
            res.ttsResponse = (res.targetAction == "CLOSE_WINDOW") ? "车窗已为您关闭。" : "车窗已为您开启。";
            res.executeCAN = true;
            return true;
        }

        return false;
    }

    std::shared_ptr<LocalMemoryEngine> memory_;
};

} // namespace edge_agent
