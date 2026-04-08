### ✨ “泄漏” 与 “检测” 定义
您的 “个人信息” 出现在被 “互联网” 广泛传播的 “部分” 数据中.

---

### 📢 宣言
1. “不记录”「查询记录」
2. “不提供”「更多信息」
3. “别忘记”「舆论监督」

记住: 你有权了解你的数据处于何种状态。

---

### 🚀 开发
使用我们的安装脚本, 快速构建开发环境.
```bash
git clone https://github.com/pa4uslf/leak-check.git
cd leak-check
./install.sh
```

### 🔐 安全配置

服务启动前至少配置以下环境变量:

```bash
export LEAK_CHECK_API_KEYS="replace-with-long-random-token"
export LEAK_CHECK_ALLOWED_ORIGINS="https://your-console.example.com"
```

- `LEAK_CHECK_API_KEYS`: 逗号分隔的 API Key 列表；`/` 与 `/dig/masking` 现在都必须携带。
- `LEAK_CHECK_ALLOWED_ORIGINS`: 允许跨域的前端来源；未配置时仅允许本地开发源。
- `LEAK_CHECK_RATE_LIMIT`: 可选，默认每个 IP 每 60 秒 30 次查询。
- `LEAK_CHECK_RATE_WINDOW_SECONDS`: 可选，默认 60 秒。

调用示例:

```bash
curl -X POST http://127.0.0.1:3001/leak-check/dig/masking \
  -H "Authorization: Bearer replace-with-long-random-token" \
  -H "Content-Type: application/json" \
  -d '{"q":"13800138000"}'
```

### 📊 数据库
本项目不提供 “数据拷贝”, For “数据库”, 您可以采用任何你喜欢的数据库, 本项目采用 ➡️ [SQLite](https://sqlite.org/).
```bash
cd leak-check

sqlite3 ./db/leak-check.db
```
```sql
-- 
-- 创建表
--
CREATE TABLE source (
    id INTEGER PRIMARY KEY,
    source TEXT DEFAULT NULL
);

CREATE TABLE person(
    id TEXT DEFAULT NULL,
    name TEXT DEFAULT NULL,
    receiver TEXT DEFAULT NULL,
    nickname TEXT DEFAULT NULL,
    phone TEXT DEFAULT NULL,
    address TEXT DEFAULT NULL,
    car TEXT DEFAULT NULL,
    email TEXT DEFAULT NULL,
    qq INTEGER DEFAULT NULL,
    weibo INTEGER DEFAULT NULL,
    contact TEXT DEFAULT NULL,
    company TEXT DEFAULT NULL,
    source_id INTEGER DEFAULT 0,

    FOREIGN KEY (source_id) REFERENCES source(id)
);
```

---

### 🗑️ 完全删除

如果需要完全删除:

```bash
# 删除项目目录即可
rm -rf leak-check/
```

---

### 📬 更新与反馈
- GitHub 仓库：[https://github.com/garinasset/leak-check](https://github.com/garinasset/leak-check)  
- Issues & Bug 报告：[https://github.com/garinasset/leak-check/issues](https://github.com/garinasset/leak-check/issues)

---

## 许可证

MIT License
