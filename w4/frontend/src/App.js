import { useState } from "react";

function App() {
  const [input1, setInput1] = useState("");
  const [input2, setInput2] = useState("");
  const [input3, setInput3] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleGet() {
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/get?value=" + encodeURIComponent(input1)
      );
      const text = await response.text();
      setResult(text);
    } catch (error) {
      setResult("请求失败，请先启动 Flask 后端。");
    } finally {
      setLoading(false);
    }
  }

  async function handlePost() {
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/post?param=" + encodeURIComponent(input3),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            body: input2,
          }),
        }
      );
      const text = await response.text();
      setResult(text);
    } catch (error) {
      setResult("请求失败，请先启动 Flask 后端。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="panel">
        <h1>React + Flask Demo</h1>

        <label>
          第一个输入框 GET 参数
          <input
            value={input1}
            onChange={(e) => setInput1(e.target.value)}
            placeholder="例如 hello"
          />
        </label>

        <button onClick={handleGet} disabled={loading}>
          发送 GET 请求
        </button>

        <label>
          第二个输入框 POST body
          <input
            value={input2}
            onChange={(e) => setInput2(e.target.value)}
            placeholder="例如 body-value"
          />
        </label>

        <label>
          第三个输入框 POST param
          <input
            value={input3}
            onChange={(e) => setInput3(e.target.value)}
            placeholder="例如 param-value"
          />
        </label>

        <button onClick={handlePost} disabled={loading}>
          发送 POST 请求
        </button>

        <div className="result">
          <span>后端返回</span>
          <strong>{result || "等待请求..."}</strong>
        </div>
      </section>
    </main>
  );
}

export default App;
