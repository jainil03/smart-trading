import plotly.graph_objects as go


def plot(data,symbol,interval):

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(

        x=data.index,

        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],

        increasing=dict(
            line=dict(color="#2962FF", width=1),
            fillcolor="#2962FF"
        ),

        decreasing=dict(
            line=dict(color="#000000", width=1),
            fillcolor="#000000"
        ),

        name="Price"
    ))

    fig.update_layout(

        height=900,
        margin=dict(
            l=0,
            r=0,
            t=30,
            b=0
        ),

        plot_bgcolor="#e6e6e6",
        paper_bgcolor="#e6e6e6",
        dragmode="pan",
        hovermode="x",

        font=dict(
            family="Arial",
            size=12,
            color="#333333"
        ),

        xaxis=dict(

            rangeslider=dict(visible=False),
            showgrid=True,
            gridcolor="#c8c8c8",
            zeroline=False

        ),

        yaxis=dict(

            side="right",
            showgrid=True,
            gridcolor="#c8c8c8",
            fixedrange=False,
            zeroline=False
        ),

        title=dict(
            text=f"{symbol} {interval.upper()}",
            x=0.01,
            y=0.98,
            xanchor="left",
            yanchor="top"
        )
    )

    fig.show(

        config={

            "scrollZoom": True,

            "displaylogo": False,

            # "modeBarButtonsToAdd": [
            #     "drawline",
            #     "drawrect"
            # ],
        }
    )