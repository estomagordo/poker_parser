import pygal


def plot_tournaments(tournaments, file):
    cumulative = []

    for t in tournaments:
        if not cumulative:
            cumulative.append(t.hero_result_cents / 100.0)
        else:
            cumulative.append(cumulative[-1] + t.hero_result_cents / 100.0)

    line_chart = pygal.Line()
    line_chart.title = 'Tournament results'
    line_chart.x_labels = map(str, range(1, len(tournaments) + 1))
    line_chart.add('$1.90 + $0.10 6-man hyper DoN', cumulative)
    line_chart.render_to_file(file)