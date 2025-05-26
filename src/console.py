import colorama as CLR
import consts as C

class Console:
    def __init__(self) -> None:
        self.counter: int = 0
        return 
    
    def print(self, *args, **kwargs) -> None:
        self.counter += 1
        print(*args, **kwargs)

    def refresh(self) -> None:
        if self.counter > 0:
            for _ in range(self.counter):
                print(C.LINE_UP + C.LINE_CLEAR, end="")
        self.counter = 0

    def reprint(self, *args, **kwargs) -> None:
        self.refresh()
        self.print(*args, **kwargs)
        return
    
    def input_str(self, *args, **kwargs) -> str:
        self.counter += 1
        return input(*args, **kwargs)
    
    def input_int(self, *args, **kwargs) -> int:
        while True:
            try:
                ret = int(self.input_str(*args, **kwargs))
                if ret < 0:
                    raise ValueError("Negative value")
                if ret > 16:
                    raise ValueError("Value too large")
                return ret
            except ValueError as e:
                self.print(f"{CLR.Fore.RED}Invalid input. Please enter an number (1..16).{CLR.Style.RESET_ALL}")
                continue