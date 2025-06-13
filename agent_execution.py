async def generate_code(prompt: str) -> str:
    # Жишээ код үүсгэгч (AI simulation)
    return (
        "```python\\n"
        "# Автоматаар үүсгэсэн код:\\n"
        "def hello():\\n"
        "    print('Hello from AI-generated code!')\\n"
        "hello()\\n"
        "```"
    )

async def execute_code(code: str) -> str:
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return f"✅ Код амжилттай гүйцэтгэсэн: {local_vars}"
    except Exception as e:
        return f"❌ Код гүйцэтгэл амжилтгүй: {str(e)}"