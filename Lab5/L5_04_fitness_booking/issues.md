# Static analysis findings

Line numbers below refer to the original `gym_system.py` baseline so they match the saved reports.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command execution | Security, high | 35–36 | `os.system` built a shell command using a string prefix, which could allow command injection and depended on a platform-specific shell command. | Replaced the shell call with `Path.glob` and `Path.unlink` to remove matching JSON files directly. |
| Capacity boundary allows an extra booking | Bug, high | 11 | The `>` test allowed a booking when the roster already equaled its capacity. | Check `len(roster) >= capacity` before appending. |
| Invalid and unknown class capacities | Bug, medium | 11, 24–25, 49 | Unknown classes defaulted to capacity zero but could still get one booking; negative capacities were accepted. | Reject unknown classes and validate that capacities are non-negative integers. |
| Unsafe mutable default argument | Bug, medium | 8, 15 | `attendance_log=[]` reused the same list across calls. | Use `None` as the default and append only when a caller supplies a log. |
| Bare exception during cancellation | Quality, medium | 18–22 | A bare `except` hid every error, including unrelated programming mistakes. | Check whether the class and member exist before removing; return a success flag. |
| Walk-in input can crash the program | Bug, medium | 52–53 | Direct integer conversion crashed on non-numeric input, and negative counts were accepted. | Catch `ValueError` and validate the guest count as a non-negative integer. |
| Export file handling | Quality, low | 31–33 | The file was not managed with a context manager and used an implicit encoding. | Use `Path.open` in a `with` block and specify UTF-8. |
| Style, naming, and documentation | Quality, low | 1, 8, 18, 24, 27, 31, 38, 42, 52 | Missing docstrings, non-snake-case names, old string formatting, and spacing issues reduced readability and triggered analyzer warnings. | Add module/function docstrings, use snake_case and f-strings, iterate with `.items()`, and format consistently. |
