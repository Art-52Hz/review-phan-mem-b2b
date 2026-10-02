"""Planning scenarios, not observed metrics or commission promises."""
import json
import math

def acquisition(target, commission, click_rate, conversion_rate):
    sales = math.ceil(target / commission)
    clicks = math.ceil(sales / conversion_rate)
    visits = math.ceil(clicks / click_rate)
    return dict(sales=sales, affiliate_clicks=clicks, qualified_visits=visits,
                estimated_commission=round(sales * commission, 2),
                revenue_per_visit=round(click_rate * conversion_rate * commission, 4))

def recurring(months, new_per_month, monthly_commission, retention):
    active = 0; result = []
    for month in range(1, months + 1):
        active = active * retention + new_per_month
        result.append(dict(month=month, expected_active=round(active, 2),
                           commission=round(active * monthly_commission, 2)))
    return result

if __name__ == '__main__':
    print(json.dumps({
        'all_inputs_are_hypothetical': True,
        'one_time_40_usd': {
            'weak': acquisition(1000, 40, .04, .01),
            'base': acquisition(1000, 40, .08, .02),
            'strong': acquisition(1000, 40, .12, .03)},
        'annual_plan_example': acquisition(1000, 144 * .30 * .85, .08, .02),
        'recurring_22_new_10_usd_92pct_retention': recurring(9, 22, 10, .92),
        'recurring_monthly_acquisition': acquisition(220, 10, .10, .02),
        'legacy_example_corrected': 30 * 500 * .04 * .025 * 35
    }, indent=2))
