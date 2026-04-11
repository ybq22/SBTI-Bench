# 批量评测断点续跑功能

## ✅ 新增功能

批量评测脚本现在支持**断点续跑**，自动跳过已经评测过的模型，节省API调用和时间。

---

## 🚀 使用方法

### 1. 默认模式：跳过已评测的模型

```bash
./batch_scripts/batch_eval.sh
```

**行为：**
- 检查 `data/results.json` 中已评测的模型
- 自动跳过已存在的模型
- 只评测新的模型

**输出示例：**
```
================================
批量评测配置
================================
模式: 跳过已评测的模型 (默认)
      使用 --force 强制重新评测

待评测模型列表（共 22 个）:
  1. openai/gpt-5.4 [已评测，将跳过]
  2. openai/gpt-4 [已评测，将跳过]
  3. anthropic/claude-opus-4.6-fast [已评测，将跳过]
  ...
  15. qwen/qwen3-max          ← 新模型，将评测
  16. deepseek/deepseek-r1    [已评测，将跳过]
  ...

开始时间: Sat Apr 11 19:17:56 CST 2026
需要评测: 2 / 22 个模型

[1/22] ⊞ 跳过已评测: openai/gpt-5.4
[2/22] ⊞ 跳过已评测: openai/gpt-4
...
[15/22] [1/2] 正在评测: qwen/qwen3-max
================================
```

### 2. 强制重新评测所有模型

```bash
./batch_scripts/batch_eval.sh --force
```

**行为：**
- 忽略已有的评测结果
- 重新评测所有模型
- 覆盖 `data/results.json` 中的旧数据

**适用场景：**
- 更新了评测算法
- 修复了bug需要重新评测
- 想要更新所有模型的评测结果

### 3. 自定义模型列表

```bash
./batch_scripts/batch_eval.sh "openai/gpt-5" "anthropic/claude-opus-4.6-fast"
```

**行为：**
- 只评测指定的模型
- 仍然会跳过已评测的模型（除非使用 `--force`）

---

## 📊 评测进度显示

脚本会实时显示：
- **总模型数**：配置文件中的模型总数
- **已评测**：本次评测完成的模型数
- **跳过**：跳过的模型数
- **进度**：当前模型位置

**示例输出：**
```
[15/22] [1/2] 正在评测: qwen/qwen3-max
================================
```
- `[15/22]`：第15个模型，总共22个
- `[1/2]`：本次需要评测2个模型，当前第1个

---

## 🎯 使用场景

### 场景1：增量评测

你已经有10个模型的评测结果，现在想评测5个新模型：

```bash
# 1. 编辑 models.conf，添加新模型
vim batch_scripts/models.conf

# 2. 直接运行（自动跳过已评测的）
./batch_scripts/batch_eval.sh
```

### 场景2：重新评测单个模型

某个模型的评测失败了，你想重新评测它：

```bash
# 方法1：手动评测单个模型
conda activate sbti
python -m backend.evaluator "ModelName" "model-id"

# 方法2：使用 --force 强制重新评测所有
./batch_scripts/batch_eval.sh --force

# 方法3：删除该模型的评测结果，然后正常运行
# 编辑 data/results.json，删除该模型的条目
./batch_scripts/batch_eval.sh
```

### 场景3：继续中断的批量评测

批量评测进行到一半被中断了（网络问题、手动停止等）：

```bash
# 直接重新运行即可，会自动跳过已完成的模型
./batch_scripts/batch_eval.sh
```

---

## 🔍 查看已评测的模型

### 方法1：运行脚本时查看

```
已评测 13 个模型:
    • GPT-4 (openai/gpt-4)
    • gpt-5_4 (openai/gpt-5.4)
    • claude-opus-4_6-fast (anthropic/claude-opus-4.6-fast)
    ...
```

### 方法2：命令行查询

```bash
# 查看已评测模型数量
cat data/results.json | jq '.total_evaluations'

# 查看所有已评测模型
cat data/results.json | jq '.evaluations[] | {name: .model_name, id: .model_id}'

# 查看特定模型是否已评测
cat data/results.json | jq '.evaluations[].model_id' | grep -q "openai/gpt-5" && echo "已评测" || echo "未评测"
```

---

## ⚙️ 配置选项

### 环境变量

无特殊环境变量要求，使用 `.env` 中的配置：

```bash
OPENROUTER_API_KEY=your_key
DEFAULT_MODEL=z-ai/glm-5.1
DEFAULT_MAX_TOKENS=1000
DEFAULT_TIMEOUT=120
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 无参数 | 跳过已评测的模型 | ✅ |
| `--force` | 强制重新评测所有模型 | ❌ |
| `model1 model2 ...` | 自定义模型列表 | 使用配置文件 |

---

## 📝 注意事项

1. **模型匹配逻辑**
   - 通过 `model_id` 匹配（如 `openai/gpt-4`）
   - 不区分 `model_name`（可以有多个同名模型）

2. **评测结果追加**
   - 新评测结果会追加到 `data/results.json`
   - 不会删除或修改已有的评测记录

3. **重复评测**
   - 同一个模型多次运行会产生多条记录
   - 使用 `--force` 会追加新的评测记录

4. **清理旧结果**
   ```bash
   # 备份当前结果
   cp data/results.json data/results_backup.json

   # 手动编辑删除不需要的记录
   vim data/results.json

   # 或使用 jq 工具
   cat data/results.json | jq '{...evaluations: .evaluations[:-1]}' > data/results_new.json
   ```

---

## 🛠️ 故障排查

### Q: 为什么所有模型都被跳过了？

**A**: 可能原因：
1. 所有模型都已经评测过了
2. `model_id` 不匹配（检查配置文件中的ID是否正确）

**解决方案**：
```bash
# 查看已评测的model_id
cat data/results.json | jq '.evaluations[].model_id' | sort -u

# 使用 --force 强制重新评测
./batch_scripts/batch_eval.sh --force
```

### Q: 如何删除某个模型的评测结果？

**A**: 使用 jq 工具：
```bash
# 删除特定模型的评测记录
cat data/results.json | jq '
    del(.evaluations[] | select(.model_id == "openai/gpt-5.4"))
    | .total_evaluations -= 1
' > data/results_new.json

mv data/results_new.json data/results.json
```

### Q: 批量评测中断后如何继续？

**A**: 直接重新运行即可：
```bash
./batch_scripts/batch_eval.sh
```

脚本会自动：
- 跳过已完成的模型
- 从中断的位置继续
- 保留之前的评测结果

---

## 📊 性能对比

| 场景 | 无断点续跑 | 有断点续跑 |
|------|-----------|-----------|
| 评测10个新模型（已有10个） | 20个模型 × 2分钟 = 40分钟 | 10个模型 × 2分钟 = 20分钟 |
| 网络中断后继续 | 从头开始（浪费已完成的） | 跳过已完成的，继续未完成的 |
| API费用 | 重复调用浪费API费用 | 节省50%+ API费用 |

---

## ✨ 总结

断点续跑功能让批量评测更加高效和可靠：

✅ **智能跳过**：自动识别已评测的模型
✅ **节省成本**：避免重复API调用
✅ **容错恢复**：中断后可以继续
✅ **灵活控制**：支持强制重新评测

现在你可以放心地运行批量评测，不用担心中断或重复评测了！🎉
