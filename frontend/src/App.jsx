import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Привет! Я AI-консультант TechBox. Помогу найти товар, сравнить варианты и оформить заказ.",
    },
  ]);

  const [message, setMessage] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  async function loadProducts() {
    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/products`);

      if (!response.ok) {
        throw new Error("Не удалось загрузить товары");
      }

      const data = await response.json();

      setProducts(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function searchProducts() {
    try {
      setLoading(true);

      const query = search.trim().replace(/\s+/g, " ");
      setSearch(query);

      if (!query) {
        await loadProducts();
        return;
      }

      const response = await fetch(
        `${API_URL}/products/search?query=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error("Ошибка поиска");
      }

      const data = await response.json();

      setProducts(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function sendMessage() {
    if (!message.trim() || chatLoading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: message,
    };

    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);
    setMessage("");
    setChatLoading(true);

    try {
      const history = updatedMessages
        .slice(0, -1)
        .map((item) => ({
          role: item.role,
          content: item.content,
        }));

      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          history,
        }),
      });

      if (!response.ok) {
        throw new Error("Ошибка AI");
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.message,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: "Не удалось получить ответ от AI.",
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          Tech<span>Box</span>
        </div>

        <div className="header-text">
          Electronics Store
        </div>
      </header>

      <main className="main">
        <section className="catalog-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">TECHBOX CATALOG</p>
              <h1>Электроника для твоего сетапа</h1>
              <p className="subtitle">
                Наушники, клавиатуры, мыши и зарядные устройства
              </p>
            </div>
          </div>

          <div className="search-box">
            <input
              type="text"
              placeholder="Поиск товара..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  searchProducts();
                }
              }}
            />

            <button onClick={searchProducts}>
              Найти
            </button>
          </div>

          {loading ? (
            <p className="status-text">
              Загружаем товары...
            </p>
          ) : products.length === 0 ? (
            <p className="status-text">
              По запросу «{search}» товары не найдены.
            </p>
          ) : (
            <div className="products-grid">
              {products.map((product) => (
                <article
                  className="product-card"
                  key={product.id}
                >
                  <div className="product-image">
                    {product.image_url ? (
                      <img
                        src={product.image_url}
                        alt={product.name}
                      />
                    ) : (
                      <span>TECHBOX</span>
                    )}
                  </div>

                  <div className="product-content">
                    <div className="product-category">
                      {product.category}
                    </div>

                    <h2>{product.name}</h2>

                    {product.brand && (
                      <p className="brand">
                        {product.brand}
                      </p>
                    )}

                    {product.description && (
                      <p className="description">
                        {product.description}
                      </p>
                    )}

                    <div className="specifications">
                      {Object.entries(
                        product.specifications || {}
                      )
                        .slice(0, 3)
                        .map(([key, value]) => (
                          <div
                            className="spec"
                            key={key}
                          >
                            <span>{key}</span>
                            <strong>
                              {String(value)}
                            </strong>
                          </div>
                        ))}
                    </div>

                    <div className="product-bottom">
                      <div>
                        <div className="price">
                          {product.price.toLocaleString()} ₸
                        </div>

                        <div
                          className={
                            product.stock > 0
                              ? "stock available"
                              : "stock unavailable"
                          }
                        >
                          {product.stock > 0
                            ? `В наличии: ${product.stock}`
                            : "Нет в наличии"}
                        </div>
                      </div>

                      <button
                        className="ask-button"
                        onClick={() => {
                          setMessage(
                            `Расскажи подробнее про ${product.name}`
                          );
                        }}
                      >
                        Спросить AI
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <aside className="ai-panel">
          <div className="ai-header">
            <div>
              <div className="ai-title">
                TechBox AI
              </div>

              <div className="ai-status">
                <span />
                online
              </div>
            </div>
          </div>

          <div className="chat">
            {messages.map((item, index) => (
              <div
                key={index}
                className={`message ${item.role}`}
              >
                {item.content}
              </div>
            ))}

            {chatLoading && (
              <div className="message assistant">
                Думаю...
              </div>
            )}
          </div>

          <div className="chat-input">
            <textarea
              placeholder="Напиши AI..."
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={handleKeyDown}
            />

            <button
              onClick={sendMessage}
              disabled={chatLoading}
            >
              Отправить
            </button>
          </div>
        </aside>
      </main>
    </div>
  );
}

export default App;
