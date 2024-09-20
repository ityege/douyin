# Linux环境编译ffmpeg库(windows在msys下通用)

# 背景说明

项目功能实现需要在Linux下编译出可用的FFmpeg库。FFmpeg在编译过程中是需要链接其它三方库的，比如x265 x265等，否则可能会造成功能不全（如程序接口返回找不到H264编码器错误），影响使用。编译这种三方库其实理论简单，但是细节磨人，有时候没设置好就是会有些莫名其妙的问题。我这里也参考了如零声学院分享的文档，结合自己情况总结记录了份编译说明，亲测有效，使用稳定。甚至可以按步骤无脑复制shell执行，编译一路绿灯，快速得到完美的FFmpeg库。

# 编译

整体思路就是先把依赖的库如x264、x265等先配置好，这些库不是必须的，但是保证库功能完整性最好都配置好。接下来就是下载FFmpeg源码，和依赖库进行配置然后进行编译，编译完成库即可用了。当前环境是 ubuntu18 desktop + ffmpeg 4.2.1

# 注意

（1）所有操作以我的环境为准，但可以完全按以下步骤依次复制命令执行，因为我是在home目录是通用的，建议按照此方法。如果想使用自己的路径要注意修改命令参数，防止路径不同造成的错误

（2）部分库可能需要连接github,最好选择网络较好的机器上编译

（3）整个安装过程，基本就是复制命令执行，等待执行结束。。。循环。测试多台机器编译过程中均无报错，正常情况预计用时15分钟以内，即可完成全部编译工作

# 一、创建目录

在home目录下创建

ffmpeg_sources：用于下载源文件

ffmpeg_build： 存储编译后的库文件

bin：存储二进制文件（ffmpeg，ffplay，ffprobe，X264，X265等）

命令：

~~~shell
cd ~ 
mkdir ffmpeg_sources  ffmpeg_build bin
~~~

# 二、安装依赖

更新软件信息

~~~shell
sudo apt-get update
~~~

安装需要的组件

~~~shell
sudo apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libass-dev \
  libfreetype6-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  pkg-config \
  texinfo \
  wget \
  zlib1g-dev
~~~

# 三、安装三方库

安装一些最常见的第三方库，默认均以源码方式安装。安装库所需的命令如下

**NASM**
部分库使用到汇编程序。
使用源码进行安装

~~~shell
cd ~/ffmpeg_sources && \
wget https://www.nasm.us/pub/nasm/releasebuilds/2.14.02/nasm-2.14.02.tar.bz2 && \
tar xjvf nasm-2.14.02.tar.bz2 && \
cd nasm-2.14.02 && \
./autogen.sh && \
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" && \
make && \
make install
~~~

**Yasm**
部分库使用到该汇编库
使用源码进行安装:

~~~shell
cd ~/ffmpeg_sources && \
wget -O yasm-1.3.0.tar.gz https://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz && \
tar xzvf yasm-1.3.0.tar.gz && \
cd yasm-1.3.0 && \
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" && \
make && \
make install
~~~

**libx264**

H.264视频编码器。更多信息和使用范例参考H.264 Encoding Guide

要求编译ffmpeg时配置：–enable-gpl --enable-libx264.

使用源码进行编译：

~~~shell
cd ~/ffmpeg_sources && \
git -C x264 pull 2> /dev/null || git clone --depth 1 https://gitee.com/mirrors_addons/x264.git && \
cd x264 && \
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static --enable-pic && \
PATH="$HOME/bin:$PATH" make && \
make install
~~~

**libx265**
H.265/HEVC 视频编码器， 更多信息和使用范例参考H.265 Encoding Guide。
要求编译ffmpeg时配置：–enable-gpl --enable-libx265.
使用源码进行编译：

~~~shell
sudo apt-get install mercurial libnuma-dev && \
cd ~/ffmpeg_sources && \
if cd x265 2> /dev/null; then git pull && cd ..; else git clone https://gitee.com/mirrors_videolan/x265.git; fi && \
cd x265/build/linux && \
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED=off ../../source && \
PATH="$HOME/bin:$PATH" make && \
make install
~~~

**libvpx**

VP8/VP9视频编解码器。 更多信息和使用范例参考VP9 Video Encoding Guide 。

要求编译ffmpeg时配置： --enable-libvpx.

使用源码进行编译：

~~~shell
cd ~/ffmpeg_sources && \
git -C libvpx pull 2> /dev/null || git clone --depth 1 https://github.com/webmproject/libvpx.git && \
cd libvpx && \
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm --enable-pic && \
PATH="$HOME/bin:$PATH" make && \
make install
~~~

libfdk-aac

AAC音频编码器. 更多信息和使用范例参考AAC Audio Encoding Guide。

要求编译ffmpeg时配置：–enable-libfdk-aac ( 如果你已经配置了 --enable-gpl则需要加上–enable-nonfree).

使用源码进行编译:

~~~shell
cd ~/ffmpeg_sources && \
git -C fdk-aac pull 2> /dev/null || git clone --depth 1 https://github.com/mstorsjo/fdk-aac && \
cd fdk-aac && \
autoreconf -fiv && \
./configure CFLAGS=-fPIC --prefix="$HOME/ffmpeg_build"   && \
make && \
make install
~~~

**libmp3lame**
MP3音频编码器.
要求编译ffmpeg时配置：–enable-libmp3lame.
使用源码进行编译：

~~~shell
cd ~/ffmpeg_sources && \
git clone  --depth 1 https://gitee.com/hqiu/lame.git && \
cd lame && \
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin"  --enable-nasm --with-pic && \
PATH="$HOME/bin:$PATH" make && \
make install
~~~

**libopus**
Opus音频编解码器.
要求编译ffmpeg时配置：–enable-libopus.
使用源码进行编译：

~~~shell
cd ~/ffmpeg_sources && \
git -C opus pull 2> /dev/null || git clone --depth 1 https://github.com/xiph/opus.git && \
cd opus && \
./autogen.sh && \
./configure --prefix="$HOME/ffmpeg_build"  -with-pic&& \
make && \
make install
~~~

# 四、安装FFmpeg

到这里常见的三方库默认已经都装好了，唠叨下，上面的库可以不全安装，但是为了库的功能全面性，还是别偷懒，毕竟编译好，可以一直用。下面下载FFmpeg源码和上面的库联合编译，此过程相对用时久一些，耐心等待

~~~shell
cd ~/ffmpeg_sources && \
wget -O ffmpeg-6.0.tar.bz2 https://ffmpeg.org/releases/ffmpeg-6.0.tar.bz2 && \
tar xjvf ffmpeg-6.0.tar.bz2 && \
cd ffmpeg-6.0 && \
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" CFLAGS="-O3 -fPIC" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-pic \
  --enable-shared   \
  --enable-nonfree && \
PATH="$HOME/bin:$PATH" make && \
make install && \
hash -r
~~~

# 问题1:

将ffmpeg源码中 mathops.h 中的如下代码做一个修改，其实在新版本的ffmpeg中已经修复了这个问题，可以去查看一下最新版的ffmpeg中 libavcodec/x86/mathops.h 中的修改，然后将我们的mathops.h 修改为如下

~~~c
#define MULL MULL
static av_always_inline av_const int MULL(int a, int b, unsigned shift)
{
    int rt, dummy;
    __asm__ (
        "imull %3               \n\t"
        "shrdl %4, %%edx, %%eax \n\t"
        :"=a"(rt), "=d"(dummy)
        :"a"(a), "rm"(b), "c"((uint8_t)shift)
    );
    return rt;
}
~~~

~~~c
#define NEG_SSR32 NEG_SSR32
static inline  int32_t NEG_SSR32( int32_t a, int8_t s){
    __asm__ ("sarl %1, %0\n\t"
         : "+r" (a)
         : "c" ((uint8_t)(-s))
    );
    return a;
}

#define NEG_USR32 NEG_USR32
static inline uint32_t NEG_USR32(uint32_t a, int8_t s){
    __asm__ ("shrl %1, %0\n\t"
         : "+r" (a)
         : "c" ((uint8_t)(-s))
    );
    return a;
}
~~~

# 问题2:

添加hevc格式的支持

https://github.com/runner365/ffmpeg_rtmp_h265

只需要把flv.h/flvdec.c/flvenc.c拷贝入libavformat文件夹中，后面ffmpeg正常编译即可。
