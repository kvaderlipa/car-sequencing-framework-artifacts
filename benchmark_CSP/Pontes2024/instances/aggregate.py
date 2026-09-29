import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------

MONTH_ORDER = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

INPUT_PATTERN = re.compile(
    r"^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)_"
    r"(\d+)_"
    r"(\d+)\.in$",
    re.IGNORECASE
)


# -------------------------------------------------------------------------
# Data structures
# -------------------------------------------------------------------------

@dataclass
class CarClass:
    class_id: int
    demand: int
    options: tuple[int, ...]


@dataclass
class CSPInstance:
    source_file: Path
    month: str
    shift_index: int
    cars_from_name: int
    number_of_cars: int
    number_of_options: int
    number_of_classes: int
    capacities: tuple[int, ...]
    window_sizes: tuple[int, ...]
    classes: list[CarClass]


# -------------------------------------------------------------------------
# Input parsing
# -------------------------------------------------------------------------

def parse_integer_line(line: str) -> list[int]:
    """
    Parse all integer values from one line.

    The parser tolerates additional textual labels or comments, for example:

        0 #carsPerClass 1 1 0 0 0 0

    becomes:

        [0, 1, 1, 0, 0, 0, 0]
    """
    return [int(value) for value in re.findall(r"-?\d+", line)]


def read_nonempty_lines(file_path: Path) -> list[str]:
    """
    Read non-empty lines from an instance file.
    """
    with file_path.open("r", encoding="utf-8-sig") as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def parse_filename(file_path: Path) -> tuple[str, int, int]:
    """
    Parse a filename such as:

        jan_15_250.in

    Returns:

        ("jan", 15, 250)
    """
    match = INPUT_PATTERN.match(file_path.name)

    if not match:
        raise ValueError(
            f"Unsupported input filename: {file_path.name}\n"
            "Expected format: month_shift_cars.in, "
            "for example jan_15_250.in"
        )

    month = match.group(1).lower()
    shift_index = int(match.group(2))
    cars_from_name = int(match.group(3))

    return month, shift_index, cars_from_name


def parse_instance(file_path: Path) -> CSPInstance:
    """
    Parse one classical CSP instance.

    Expected structure:

        numberOfCars numberOfOptions numberOfClasses
        H_1 ... H_o
        N_1 ... N_o
        classId demand option_1 ... option_o
        ...
    """
    month, shift_index, cars_from_name = parse_filename(file_path)
    lines = read_nonempty_lines(file_path)

    if len(lines) < 3:
        raise ValueError(
            f"{file_path.name}: expected at least three header lines."
        )

    header = parse_integer_line(lines[0])

    if len(header) != 3:
        raise ValueError(
            f"{file_path.name}: the first line must contain exactly "
            "numberOfCars, numberOfOptions and numberOfClasses."
        )

    number_of_cars, number_of_options, number_of_classes = header

    capacities = parse_integer_line(lines[1])
    window_sizes = parse_integer_line(lines[2])

    if len(capacities) != number_of_options:
        raise ValueError(
            f"{file_path.name}: expected {number_of_options} option "
            f"capacities, found {len(capacities)}."
        )

    if len(window_sizes) != number_of_options:
        raise ValueError(
            f"{file_path.name}: expected {number_of_options} window "
            f"sizes, found {len(window_sizes)}."
        )

    class_lines = lines[3:]

    if len(class_lines) != number_of_classes:
        raise ValueError(
            f"{file_path.name}: expected {number_of_classes} class "
            f"lines, found {len(class_lines)}."
        )

    classes = []

    for line_number, line in enumerate(class_lines, start=4):
        values = parse_integer_line(line)
        expected_values = number_of_options + 2

        if len(values) != expected_values:
            raise ValueError(
                f"{file_path.name}, line {line_number}: expected "
                f"{expected_values} integer values, found {len(values)}."
            )

        class_id = values[0]
        demand = values[1]
        options = tuple(values[2:])

        classes.append(
            CarClass(
                class_id=class_id,
                demand=demand,
                options=options
            )
        )

    demand_sum = sum(car_class.demand for car_class in classes)

    if demand_sum != number_of_cars:
        raise ValueError(
            f"{file_path.name}: sum of class demands is {demand_sum}, "
            f"but the header specifies {number_of_cars} cars."
        )

    if cars_from_name != number_of_cars:
        print(
            f"WARNING: {file_path.name}: filename contains "
            f"{cars_from_name} cars, but the file header contains "
            f"{number_of_cars} cars."
        )

    return CSPInstance(
        source_file=file_path,
        month=month,
        shift_index=shift_index,
        cars_from_name=cars_from_name,
        number_of_cars=number_of_cars,
        number_of_options=number_of_options,
        number_of_classes=number_of_classes,
        capacities=tuple(capacities),
        window_sizes=tuple(window_sizes),
        classes=classes
    )


# -------------------------------------------------------------------------
# Sorting and compatibility validation
# -------------------------------------------------------------------------

def instance_sort_key(instance: CSPInstance):
    """
    Sort instances chronologically by month and then numerically
    by shift index.
    """
    return (
        MONTH_ORDER[instance.month],
        instance.shift_index
    )


def validate_compatibility(
    reference: CSPInstance,
    candidate: CSPInstance
):
    """
    Ensure that only class demands differ between two instances.
    """
    if candidate.number_of_options != reference.number_of_options:
        raise ValueError(
            f"{candidate.source_file.name}: number of options differs "
            f"from {reference.source_file.name}."
        )

    if candidate.number_of_classes != reference.number_of_classes:
        raise ValueError(
            f"{candidate.source_file.name}: number of classes differs "
            f"from {reference.source_file.name}."
        )

    if candidate.capacities != reference.capacities:
        raise ValueError(
            f"{candidate.source_file.name}: option capacities differ "
            f"from {reference.source_file.name}."
        )

    if candidate.window_sizes != reference.window_sizes:
        raise ValueError(
            f"{candidate.source_file.name}: window sizes differ "
            f"from {reference.source_file.name}."
        )

    reference_classes = {
        car_class.class_id: car_class
        for car_class in reference.classes
    }

    candidate_classes = {
        car_class.class_id: car_class
        for car_class in candidate.classes
    }

    if set(reference_classes) != set(candidate_classes):
        raise ValueError(
            f"{candidate.source_file.name}: class IDs differ from "
            f"{reference.source_file.name}."
        )

    for class_id, reference_class in reference_classes.items():
        candidate_class = candidate_classes[class_id]

        if candidate_class.options != reference_class.options:
            raise ValueError(
                f"{candidate.source_file.name}: option signature of "
                f"class {class_id} differs from "
                f"{reference.source_file.name}."
            )


# -------------------------------------------------------------------------
# Aggregation
# -------------------------------------------------------------------------

def create_aggregated_instance(
    instances: list[CSPInstance],
    reference: CSPInstance
) -> CSPInstance:
    """
    Aggregate class demands over multiple consecutive shifts.
    """
    aggregated_demands = {
        car_class.class_id: 0
        for car_class in reference.classes
    }

    total_cars = 0

    for instance in instances:
        total_cars += instance.number_of_cars

        for car_class in instance.classes:
            aggregated_demands[car_class.class_id] += car_class.demand

    aggregated_classes = []

    for reference_class in reference.classes:
        aggregated_classes.append(
            CarClass(
                class_id=reference_class.class_id,
                demand=aggregated_demands[reference_class.class_id],
                options=reference_class.options
            )
        )

    demand_sum = sum(
        car_class.demand
        for car_class in aggregated_classes
    )

    if demand_sum != total_cars:
        raise ValueError(
            f"Internal aggregation error: total demand is {demand_sum}, "
            f"but total number of cars is {total_cars}."
        )

    return CSPInstance(
        source_file=Path(""),
        month=instances[0].month,
        shift_index=instances[0].shift_index,
        cars_from_name=total_cars,
        number_of_cars=total_cars,
        number_of_options=reference.number_of_options,
        number_of_classes=reference.number_of_classes,
        capacities=reference.capacities,
        window_sizes=reference.window_sizes,
        classes=aggregated_classes
    )


# -------------------------------------------------------------------------
# Output
# -------------------------------------------------------------------------

def format_integer_row(values) -> str:
    return " ".join(str(value) for value in values)


def write_instance(
    instance: CSPInstance,
    output_file: Path
):
    """
    Write an aggregated instance using the original CSP notation.
    """
    with output_file.open("w", encoding="utf-8", newline="\n") as file:

        file.write(
            f"{instance.number_of_cars} "
            f"{instance.number_of_options} "
            f"{instance.number_of_classes}\n"
        )

        file.write(
            format_integer_row(instance.capacities) + "\n"
        )

        file.write(
            format_integer_row(instance.window_sizes) + "\n"
        )

        for car_class in instance.classes:
            row = [
                car_class.class_id,
                car_class.demand,
                *car_class.options
            ]

            file.write(format_integer_row(row) + "\n")


def write_aggregation_log(log_rows: list[dict], output_file: Path):
    """
    Write a reproducibility log in TSV format.
    """
    with output_file.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.writer(
            file,
            delimiter="\t",
            lineterminator="\n"
        )

        writer.writerow([
            "Output File",
            "Total Cars",
            "Number of Shifts",
            "Target Reached",
            "First Input",
            "Last Input",
            "Input Files"
        ])

        for row in log_rows:
            writer.writerow([
                row["output_file"],
                row["total_cars"],
                row["number_of_shifts"],
                row["target_reached"],
                row["first_input"],
                row["last_input"],
                "; ".join(row["input_files"])
            ])


# -------------------------------------------------------------------------
# Main program
# -------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "  python aggregate_instances.py <target_number_of_cars>\n\n"
            "Example:\n"
            "  python aggregate_instances.py 1200"
        )
        sys.exit(1)

    try:
        target_cars = int(sys.argv[1])
    except ValueError:
        print("ERROR: target number of cars must be an integer.")
        sys.exit(1)

    if target_cars <= 0:
        print("ERROR: target number of cars must be greater than zero.")
        sys.exit(1)

    current_directory = Path.cwd()

    input_files = [
        file_path
        for file_path in current_directory.glob("*.in")
        if INPUT_PATTERN.match(file_path.name)]
        
    if not input_files:
        print(
            "ERROR: no compatible *.in files found in:\n"
            f"  {current_directory}\n\n"
            "Expected filenames such as:\n"
            "  jan_0_103.in\n"
            "  feb_12_203.in"
        )
        sys.exit(1)

    print(f"Current directory: {current_directory}")
    print(f"Target number of cars: {target_cars}")
    print(f"Input files found: {len(input_files)}")
    print()

    # Parse all input files.
    parsed_instances = []

    for input_file in input_files:
        instance = parse_instance(input_file)

        # Skip zero-demand shifts completely.
        if instance.number_of_cars == 0:
            print(f"SKIP ZERO DEMAND: {input_file.name}")
            continue

        parsed_instances.append(instance)

    if not parsed_instances:
        print("ERROR: all input files have zero demand.")
        sys.exit(1)

    # Sort chronologically across month boundaries.
    parsed_instances.sort(key=instance_sort_key)

    reference = parsed_instances[0]

    # Validate all invariant model components.
    for instance in parsed_instances[1:]:
        validate_compatibility(reference, instance)

    print()
    print("Compatibility validation successful.")
    print(f"Non-zero shifts: {len(parsed_instances)}")
    print()

    aggregate_counter = 1
    current_group = []
    current_total = 0
    log_rows = []

    for instance in parsed_instances:
        current_group.append(instance)
        current_total += instance.number_of_cars

        # Include the complete shift that reaches or exceeds the target.
        if current_total >= target_cars:
            aggregated = create_aggregated_instance(
                current_group,
                reference
            )

            output_name = (
                f"pontes_agg_{aggregate_counter:03d}_"
                f"{aggregated.number_of_cars}.txt"
            )

            output_file = current_directory / output_name
            write_instance(aggregated, output_file)

            input_names = [
                item.source_file.name
                for item in current_group
            ]

            print(
                f"CREATED: {output_name} | "
                f"cars={aggregated.number_of_cars} | "
                f"shifts={len(current_group)} | "
                f"{input_names[0]} -> {input_names[-1]}"
            )

            log_rows.append({
                "output_file": output_name,
                "total_cars": aggregated.number_of_cars,
                "number_of_shifts": len(current_group),
                "target_reached": "YES",
                "first_input": input_names[0],
                "last_input": input_names[-1],
                "input_files": input_names
            })

            aggregate_counter += 1
            current_group = []
            current_total = 0

    # Save the final group even when it is smaller than the target.
    if current_group:
        aggregated = create_aggregated_instance(
            current_group,
            reference
        )

        output_name = (
            f"pontes_agg_{aggregate_counter:03d}_"
            f"{aggregated.number_of_cars}.txt"
        )

        output_file = current_directory / output_name
        write_instance(aggregated, output_file)

        input_names = [
            item.source_file.name
            for item in current_group
        ]

        print(
            f"CREATED BELOW TARGET: {output_name} | "
            f"cars={aggregated.number_of_cars} | "
            f"shifts={len(current_group)} | "
            f"{input_names[0]} -> {input_names[-1]}"
        )

        log_rows.append({
            "output_file": output_name,
            "total_cars": aggregated.number_of_cars,
            "number_of_shifts": len(current_group),
            "target_reached": "NO",
            "first_input": input_names[0],
            "last_input": input_names[-1],
            "input_files": input_names
        })

    log_file = current_directory / "aggregation_log.tsv"
    write_aggregation_log(log_rows, log_file)

    print()
    print("Aggregation completed.")
    print(f"Aggregated instances created: {len(log_rows)}")
    print(f"Aggregation log: {log_file.name}")


if __name__ == "__main__":
    main()