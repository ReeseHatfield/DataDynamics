from src.parsing.DataReader import DataReader
import os
import pickle
import datetime

PRECIPITATION_THRESHOLD = 1.25  # inches of precipitation


def compute_monthly_deviation():
    # Load weather data
    weather_pickle_path = os.path.join('data', 'serialized', 'weather_data_by_day.pkl')
    weather_data = load_weather_data_from_pickle(weather_pickle_path)
    precipitation_effects = []

    # dict of {datetime.date() : (temp, precip) }
    # only includes date where business was open
    # Load sales data
    reader = DataReader(os.path.join('data', 'dataSet.csv'))

    sales_per_month = get_sales_by_month(reader)
    sales_by_date = reader.get_sales_by_day()
    print(sales_per_month)

    # Process each month
    for i in range(1, 13):
        current_month: int = i

        avg_temp = calculate_avg_temp_for_month(current_month, weather_data)
        avg_sales_on_normal_day = sales_per_month[current_month - 1]

        days_precipitated_in_current_month = [date for date in weather_data.keys()
                                              if date.month == current_month
                                              and weather_data[date][1] > PRECIPITATION_THRESHOLD]

        print(days_precipitated_in_current_month)

        average_sales_on_precip_days = calculate_sales_on_precip_days(days_precipitated_in_current_month, sales_by_date)
        if average_sales_on_precip_days is None:
            print(f"No precipitated days for month {current_month}.")
            continue

        print(f"Average sales on normal day: {avg_sales_on_normal_day}")
        print(f"Average sales on precip day: {average_sales_on_precip_days}")

        precip_effect = average_sales_on_precip_days / avg_sales_on_normal_day

        precip_effect -= 1
        precip_effect *= 100
        print(f"Precip Affect for {current_month}: {precip_effect:.2f}%")
        precipitation_effects.append(precip_effect)

    print(precipitation_effects)

    avg_precip_effect = calculate_avg_precip_effect(precipitation_effects)

    print(f"Avg precip effect: {avg_precip_effect}")


def calculate_avg_precip_effect(effects: list):
    total = 0
    divisor = len(effects)
    for current_effect in effects:
        total += abs(current_effect)

    return total / divisor


def calculate_sales_on_precip_days(days_precipitated: list, sales_by_date: dict) -> float:
    if not days_precipitated:
        return None

    total = 0
    for date in days_precipitated:
        if date in sales_by_date:
            total += sales_by_date[date]
    return total / len(days_precipitated)


def get_sales_by_month(reader: DataReader) -> list:
    sales_per_month = []

    path = os.path.join("data", "serialized", "avg_sales_per_month.pkl")

    if os.path.exists(path):
        with open(path, "rb") as f:
            sales_per_month = pickle.load(f)
            return sales_per_month
    else:
        for current_month in range(1, 13):
            avg_sales_in_in_month = reader.get_avg_sales_per_day_in_month(current_month)
            sales_per_month.append(avg_sales_in_in_month)

        with open(path, 'wb') as f:
            pickle.dump(sales_per_month, f)
    return sales_per_month


def calculate_avg_temp_for_month(month: int, weather_data: dict):
    total_temp = 0
    total_days = 0
    for date, weather in weather_data.items():
        if date.month == month:
            total_temp += weather[0]  # Assuming the second element of the tuple is temperature
            total_days += 1

    if total_days == 0:
        return None

    avg_temp = total_temp / total_days
    return avg_temp


def load_weather_data_from_pickle(weather_pickle_path: str):
    weather_data = None

    if not os.path.exists(weather_pickle_path):
        print(f"File does not exist: {weather_pickle_path}")
        raise FileNotFoundError

    try:
        with open(weather_pickle_path, 'rb') as f:
            weather_data = pickle.load(f)
    except (pickle.UnpicklingError, EOFError) as e:
        print(f"Error while reading the pickle file: {str(e)}")
        weather_data = None

    return weather_data


if __name__ == "__main__":
    compute_monthly_deviation()
