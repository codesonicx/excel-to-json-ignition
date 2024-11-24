# Excel to JSON Converter for Ignition 8.1 Alarm Automation

## Overview
This Python project was developed to streamline the process of creating structured JSON files from Excel sheets, specifically for configuring alarms in Ignition 8.1, a SCADA system. By automating this process, you can reduce the time and effort needed to manually configure alarms, ensuring consistency and accuracy.

---

## Features
- **Excel Parsing**: Reads Excel files containing alarm configuration data.
- **JSON Conversion**: Transforms Excel data into structured JSON files compatible with Ignition 8.1.
- **Automation**: Simplifies and speeds up the alarm creation process in SCADA environments.
- **Error Handling**: Ensures the integrity of the generated JSON files by validating input data.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/codesonicx/excel-to-json-ignition.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd excel-to-json-ignition
   ```
3. **Install dependencies**:
   Ensure you have Python 3.8+ installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Place your Excel file (e.g., `alarms.xlsx`) in the `input` directory.
2. Run the script:
   ```bash
   python main.py
   ```
3. The structured JSON file(s) will be generated in the `output` directory, ready for import into Ignition 8.1.

---

## Example

**Input Excel File**:  
| Tag Path                 | Description                 |
|--------------------------|-----------------------------|
| `PLC1/Temp/Area1.0`      | `Area1 Temperature High`    |
| `PLC2/Pressure[5].2`     | `Valve 5 Pressure Low`      |

**Generated JSON File**:  
```json
{
    "tags": [
        {
            "name": "PLC1",
            "tagType": "Folder",
            "tags": [
                ...
                {
                    "name": "Area1",
                    "typeId": "YOUR UDT",
                    "tagType": "UdtInstance",
                    "tags": [
                        ...
                        "0_description": "Area1 Temperature High",
                        ...
                    ]
                }
            ]
        },
        {
            "name": "PLC2",
            "tagType": "Folder",
            "tags": [
                ...
                {
                    "name": "5",
                    "typeId": "YOUR UDT",
                    "tagType": "UdtInstance",
                    "tags": [
                        ...
                        "2_description": "Valve 5 Pressure Low",
                        ...
                    ]
                }
            ]
        }
    ]
}
```

---

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.

---

## Author

👤 **Jorge Antonio Acosta Rosales**  
This project was created with the goal of improving workflows in SCADA systems by automating repetitive tasks. Feel free to reach out if you have questions or suggestions!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments

- **Ignition 8.1** by Inductive Automation for its flexible SCADA platform.
- Open-source Python libraries that made this project possible.
