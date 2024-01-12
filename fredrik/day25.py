import collections

from shared import utils


def parse_graph(graph_raw: str) -> dict[str, set[str]]:
    graph = collections.defaultdict(set)
    for line in graph_raw.splitlines():
        node, connections_raw = line.split(": ")
        connections = connections_raw.split()
        graph[node] |= set(connections)

        for connection in connections:
            graph[connection].add(node)

    return graph


def get_disjoint_groups(graph: dict[str, set[str]]) -> tuple[set[str], set[str]]:
    keys = list(graph.keys())
    partition1, partition2 = set(keys[:-1]), set(keys[-1:])

    while True:
        connections = {node: 0 for node in partition1}

        for node in partition2:
            for connection in graph[node]:
                if connection in connections:
                    connections[connection] += 1

        if sum(connections.values()) == 3:
            break

        most_connected = max(connections, key=connections.get)
        partition1.remove(most_connected)
        partition2.add(most_connected)

    return partition1, partition2


def part1(graph: dict[str, set[str]]) -> int:
    group1, group2 = get_disjoint_groups(graph=graph)
    return len(group1) * len(group2)


def main() -> None:
    graph_raw = utils.read_input_to_string()
    graph = parse_graph(graph_raw)

    print(f"Part 1: {part1(graph=graph)}")


if __name__ == "__main__":
    main()
