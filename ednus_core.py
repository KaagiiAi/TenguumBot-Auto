def generate_logical_response(user_input):
    user_input = user_input.lower()
    if "ямар" in user_input and "зориулалт" in user_input:
        return "🧠 Энэ бол AI найз таны зорилгыг тодорхойлох систем юм!"
    elif "мөнгө" in user_input:
        return "💸 Мөнгөний асуудал бол төлөвлөлт, тууштай байдал хоёрын дундах үр дүн юм."
    elif "амьдрал" in user_input:
        return "🌱 Амьдрал бол зогсолтгүй хөгжлийн аялал."
    else:
        return "🤖 Энгийн горим: Та илүү тодорхой асуулт асуугаарай."