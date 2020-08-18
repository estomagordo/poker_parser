import pygal

from collections import defaultdict


def plot_tournaments(tournaments, file):
    cumulative = defaultdict(list)

    for t in tournaments:
        buyin = '%.2f' % (t.buyin_cents / 100.0)
        rake = '%.2f' % (t.rake_cents / 100.0)
        key = f'${buyin} + {rake}'

        if not cumulative[key]:
            cumulative[key].append(t.hero_result_cents / 100.0)
        else:
            cumulative[key].append(cumulative[key][-1] + t.hero_result_cents / 100.0)

    line_chart = pygal.Line()
    line_chart.title = 'Tournament results'
    line_chart.x_labels = map(str, range(1, len(tournaments) + 1))

    for k, v in cumulative.items():
        line_chart.add(k + ' 6-man hyper DoN', v)

    line_chart.render_to_file(file)