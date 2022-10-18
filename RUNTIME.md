# Runtime tests

Tests where taken with the `./main samples/jfk.wav` command.

## Timings before optimization

```cpp
whisper_print_timings:     load time =   182.73 ms
whisper_print_timings:      mel time =    28.06 ms
whisper_print_timings:   sample time =     1.94 ms
whisper_print_timings:   encode time =   800.59 ms / 133.43 ms per layer
whisper_print_timings:   decode time =   101.05 ms / 16.84 ms per layer
whisper_print_timings:    total time =  1115.47 ms
```

## Timings after optimization

```
whisper_print_timings:    total time =   669.82 ms
```
