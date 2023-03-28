
def pm10_to_aqi(pm10):
    if pm10 < 0:
        return "Invalid input: PM10 value can't be negative."
    elif pm10 > 604:
        return "Invalid input: PM10 value can't exceed 604 µg/m³."
    elif pm10 > 500:
        aqi = ((500-401)/(604-505))*(pm10-505)+401
    elif pm10 > 350:
        aqi = ((400-301)/(504-405))*(pm10-405)+301
    elif pm10 > 250:
        aqi = ((300-201)/(404-305))*(pm10-305)+201
    elif pm10 > 150:
        aqi = ((200-151)/(304-155))*(pm10-155)+151
    elif pm10 > 55:
        aqi = ((150-101)/(154-56))*(pm10-56)+101
    elif pm10 > 35:
        aqi = ((100-51)/(54-36))*(pm10-36)+51
    elif pm10 > 0:
        aqi = ((50-0)/(35-0))*(pm10-0)+0
    else:
        return "Invalid input: PM10 value can't be zero."
    return round(aqi)


def pm25_to_aqi(pm25):
    if pm25 < 0:
        return "Invalid input: PM2.5 value can't be negative."
    elif pm25 > 500:
        return "Invalid input: PM2.5 value can't exceed 500 µg/m³."
    elif pm25 > 350.5:
        aqi = ((500-401)/(500.4-350.5))*(pm25-350.5)+401
    elif pm25 > 250.5:
        aqi = ((400-301)/(350.4-250.5))*(pm25-250.5)+301
    elif pm25 > 150.5:
        aqi = ((300-201)/(250.4-150.5))*(pm25-150.5)+201
    elif pm25 > 55.5:
        aqi = ((200-151)/(150.4-55.5))*(pm25-55.5)+151
    elif pm25 > 35.5:
        aqi = ((150-101)/(55.4-35.5))*(pm25-35.5)+101
    elif pm25 > 12.1:
        aqi = ((100-51)/(35.4-12.1))*(pm25-12.1)+51
    elif pm25 > 0:
        aqi = ((50-0)/(12-0))*(pm25-0)+0
    else:
        return "Invalid input: PM2.5 value can't be zero."
    return round(aqi)


if __name__ == "__main__":
    print(pm10_to_aqi(10.64))