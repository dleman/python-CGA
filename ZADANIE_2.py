import networkx as nx
import plotly.figure_factory as ff


def getInputFromConsole():
    result = []
    try:
        while True:
            line = input()
            result.append(line.strip())
    except EOFError:
        return result


def getInputFromFile():
    result = []
    with open("debug", "r") as f:
        for line in f:
            result.append(line.strip())
    return result


def parseInput(inputArray):
    tasks = eval(f"[{inputArray[0]}]")
    edges = eval(f"[{inputArray[1]}]")
    machinesCount = int(inputArray[2])

    return tasks, edges, machinesCount


def calcCoffmanGraham(tasks, edges):

    # create a directed graph
    graph = nx.DiGraph()
    graph.add_nodes_from(tasks)
    graph.add_edges_from(edges)

    # perform topological sort on the graph and assign it to variable
    stack = list(nx.topological_sort(graph))

    # init start times
    startTimes = {node: 0 for node in stack}

    # iterate over the tasks in the topological order
    for node in stack:
        # init max start time
        maxStartTime = 0
        # iterate over the predecessors (dependencies) of the current task
        for predecessor in graph.predecessors(node):
            # check if start time > current maximum start time
            if startTimes[predecessor] > maxStartTime:
                # update maximum start time with the start time of the predecessor
                maxStartTime = startTimes[predecessor]
        # calculate start time for the current task by adding 1 to the maximum start time
        startTimes[node] = maxStartTime + 1

    # sort tasks
    sortedTasks = sorted(startTimes.items())

    cmax = max(startTimes.values())

    # assign result
    result = {task[0]: start_time - 1 for task, start_time in sortedTasks}

    return result, cmax


def drawChart(result, machines_count, cmax):
    df = []
    for task, startTime in result.items():
        machine = startTime % machines_count + 1
        df.append(dict(Task=f'Machine {machine}', Start=int(startTime), Finish=int(startTime) + 1,
                       Resource=task))

    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=False, title='Gantt Chart')
    fig.update_layout(xaxis_type='linear', xaxis_title='Time', yaxis_title='Machine Number')

    fig.add_annotation(x=max(result.values()) + 0.5, y=-0.1, text=f'Cmax: {cmax}', showarrow=False)

    fig.show()


def run(tasks, edges, machinesCount):
    result, cmax = calcCoffmanGraham(tasks, edges)

    for i, (task, time) in enumerate(result.items()):
        print(f"'{task}': {time}", end="")
        if i < len(result) - 1:
            print(", ", end="")

    drawChart(result, machinesCount, cmax)


if __name__ == "__main__":
    # inputArr = getInputFromConsole()
    inputArr = getInputFromFile()

    tasks, edges, machinesCount = parseInput(inputArr)

    run(tasks, edges, machinesCount)