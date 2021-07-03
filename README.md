### sample project trying to recreate ts-issue (TBD)

1. run ts with docker - default loaded models are defined in "model_snapshot" parameter within the docker/config.properties file
```
docker run --rm --name ts-cpu-dummy -it -p 8080:8080 -p 8081:8081 -p 8082:8082 \
--mount type=bind,source=$(pwd)/logs/,target=/home/model-server/logs \
--mount type=bind,source=$(pwd)/model_store/,target=/home/model-server/model_store \
--mount type=bind,source=$(pwd)/docker/config.properties,target=/home/model-server/config.properties \
--mount type=bind,source=$(pwd)/docker/log4j.properties,target=/home/model-server/log4j.properties \
pytorch/torchserve:0.4.0-cpu \
torchserve \
--model-store=/home/model-server/model_store \
--ts-config config.properties \
--ncs --foreground
```

2. create conda env 
```
conda env create --force -f environment.yml

conda activate ts-issue
```

3. run the test script (make sure the docker ts dummy model is running)
```
python test.py
```
4. test script will run around 180000 requests (async) - at some point (not always the same) some worker will crash with an exception like the following (check logs/ts_log.log) 
```
2021-07-03 12:39:08,236 [ERROR] epollEventLoopGroup-5-3 org.pytorch.serve.wlm.WorkerThread - Unknown exception
io.netty.handler.codec.DecoderException: java.lang.IndexOutOfBoundsException: readerIndex(65535) + length(4) exceeds writerIndex(65536): PooledUnsafeDirectByteBuf(ridx: 65535, widx: 65536, cap: 65536)
	at io.netty.handler.codec.ByteToMessageDecoder.callDecode(ByteToMessageDecoder.java:471)
	at io.netty.handler.codec.ByteToMessageDecoder.channelRead(ByteToMessageDecoder.java:276)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:379)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:365)
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:357)
	at io.netty.channel.DefaultChannelPipeline$HeadContext.channelRead(DefaultChannelPipeline.java:1410)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:379)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:365)
	at io.netty.channel.DefaultChannelPipeline.fireChannelRead(DefaultChannelPipeline.java:919)
	at io.netty.channel.epoll.AbstractEpollStreamChannel$EpollStreamUnsafe.epollInReady(AbstractEpollStreamChannel.java:795)
	at io.netty.channel.epoll.EpollDomainSocketChannel$EpollDomainUnsafe.epollInReady(EpollDomainSocketChannel.java:138)
	at io.netty.channel.epoll.EpollEventLoop.processReady(EpollEventLoop.java:475)
	at io.netty.channel.epoll.EpollEventLoop.run(EpollEventLoop.java:378)
	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:989)
	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
	at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
	at java.base/java.lang.Thread.run(Thread.java:829)
Caused by: java.lang.IndexOutOfBoundsException: readerIndex(65535) + length(4) exceeds writerIndex(65536): PooledUnsafeDirectByteBuf(ridx: 65535, widx: 65536, cap: 65536)
	at io.netty.buffer.AbstractByteBuf.checkReadableBytes0(AbstractByteBuf.java:1478)
	at io.netty.buffer.AbstractByteBuf.readInt(AbstractByteBuf.java:811)
	at org.pytorch.serve.util.codec.ModelResponseDecoder.decode(ModelResponseDecoder.java:56)
	at io.netty.handler.codec.ByteToMessageDecoder.decodeRemovalReentryProtection(ByteToMessageDecoder.java:501)
	at io.netty.handler.codec.ByteToMessageDecoder.callDecode(ByteToMessageDecoder.java:440)
	... 16 more
2021-07-03 12:39:08,237 [INFO ] epollEventLoopGroup-5-3 org.pytorch.serve.wlm.WorkerThread - 9001 Worker disconnected. WORKER_MODEL_LOADED
2021-07-03 12:39:08,238 [DEBUG] W-9001-dummy_1.0 org.pytorch.serve.wlm.WorkerThread - System state is : WORKER_MODEL_LOADED
2021-07-03 12:39:08,238 [DEBUG] W-9001-dummy_1.0 org.pytorch.serve.wlm.WorkerThread - Backend worker monitoring thread interrupted or backend worker process died.
java.lang.InterruptedException
	at java.base/java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.reportInterruptAfterWait(AbstractQueuedSynchronizer.java:2056)
	at java.base/java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.awaitNanos(AbstractQueuedSynchronizer.java:2133)
	at java.base/java.util.concurrent.ArrayBlockingQueue.poll(ArrayBlockingQueue.java:432)
	at org.pytorch.serve.wlm.WorkerThread.run(WorkerThread.java:188)
	at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:515)
	at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
	at java.base/java.lang.Thread.run(Thread.java:829)
2021-07-03 12:39:08,238 [ERROR] epollEventLoopGroup-5-3 org.pytorch.serve.wlm.WorkerThread - Unknown exception
io.netty.handler.codec.DecoderException: java.lang.IndexOutOfBoundsException: readerIndex(65535) + length(4) exceeds writerIndex(65536): PooledUnsafeDirectByteBuf(ridx: 65535, widx: 65536, cap: 65536)
	at io.netty.handler.codec.ByteToMessageDecoder.callDecode(ByteToMessageDecoder.java:471)
	at io.netty.handler.codec.ByteToMessageDecoder.channelInputClosed(ByteToMessageDecoder.java:404)
	at io.netty.handler.codec.ByteToMessageDecoder.channelInputClosed(ByteToMessageDecoder.java:371)
	at io.netty.handler.codec.ByteToMessageDecoder.channelInactive(ByteToMessageDecoder.java:354)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelInactive(AbstractChannelHandlerContext.java:262)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelInactive(AbstractChannelHandlerContext.java:248)
	at io.netty.channel.AbstractChannelHandlerContext.fireChannelInactive(AbstractChannelHandlerContext.java:241)
	at io.netty.channel.DefaultChannelPipeline$HeadContext.channelInactive(DefaultChannelPipeline.java:1405)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelInactive(AbstractChannelHandlerContext.java:262)
	at io.netty.channel.AbstractChannelHandlerContext.invokeChannelInactive(AbstractChannelHandlerContext.java:248)
	at io.netty.channel.DefaultChannelPipeline.fireChannelInactive(DefaultChannelPipeline.java:901)
	at io.netty.channel.AbstractChannel$AbstractUnsafe$8.run(AbstractChannel.java:819)
	at io.netty.util.concurrent.AbstractEventExecutor.safeExecute(AbstractEventExecutor.java:164)
	at io.netty.util.concurrent.SingleThreadEventExecutor.runAllTasks(SingleThreadEventExecutor.java:472)
	at io.netty.channel.epoll.EpollEventLoop.run(EpollEventLoop.java:384)
	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:989)
	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
	at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
	at java.base/java.lang.Thread.run(Thread.java:829)
Caused by: java.lang.IndexOutOfBoundsException: readerIndex(65535) + length(4) exceeds writerIndex(65536): PooledUnsafeDirectByteBuf(ridx: 65535, widx: 65536, cap: 65536)
	at io.netty.buffer.AbstractByteBuf.checkReadableBytes0(AbstractByteBuf.java:1478)
	at io.netty.buffer.AbstractByteBuf.readInt(AbstractByteBuf.java:811)
	at org.pytorch.serve.util.codec.ModelResponseDecoder.decode(ModelResponseDecoder.java:56)
	at io.netty.handler.codec.ByteToMessageDecoder.decodeRemovalReentryProtection(ByteToMessageDecoder.java:501)
	at io.netty.handler.codec.ByteToMessageDecoder.callDecode(ByteToMessageDecoder.java:440)
	... 18 more
```


### (optional) model archive (not necessary - use already archived model in model_store/)
- archive our test/dummy model
```
torch-model-archiver -f --model-name dummy_nomodel --version 1.0 --handler handler_nomodel.py --serialized-file model_store/dummy.ckpt --export-path model_store/
```
