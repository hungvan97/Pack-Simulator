import sys
import time

def progressbar(it, prefix="", size=60, out=sys.stdout):# Python3.6+
    """Progress bar for any iterable
    
    Args:
        it (iterable): Any iterable object
        prefix (str, optional): Prefix string to display. Defaults to "Executing".
        size (int, optional): Size of the progress bar. Defaults to 60.
        out (file, optional): Output file. Defaults to sys.stdout.
    """
    count = len(it)
    start = time.time() # time estimate start
    def show(j) -> None:
        x = int(size*j/count)
        # time estimate calculation and string
        remaining = ((time.time() - start) / j) * (count - j)        
        mins, sec = divmod(remaining, 60) # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        print(f"{prefix} [{u'█'*x}{('.'*(size-x))}] {j}/{count} Est wait {time_str}", end='\r', file=out, flush=True)
    show(0.1) # avoid div/0 
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)   # flush data to output stream, rather than buffering it