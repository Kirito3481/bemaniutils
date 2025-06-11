<p align="center">
    <a href="./README.md">English</a> |
    <a href="./README-ko.md" style="font-weight: bold">한국어</a>
</p>

# 소개

BEMANI 시리즈의 다양한 게임 관련 작업을 위한 프로그램 모음입니다. 이것은 더 간단한 부분들을
제공하는 다양한 모듈로 상당 부분 풀어낼 수 있었지만, 시간이 흐르면서 지금과 같은 모습으로 발전하게
되었습니다. 이 리포지토리에는 다양한 파일 형식의 압축을 풀고(때로는 다시 압축하고), 다양한 게임의
네트워크 서비스를 에뮬레이트하며, 네트워크 패킷을 스니핑, 리디렉션 및 재구성하고, 다양한 게임 뮤직
데이터베이스에 대한 정보를 수집하는 유틸리티들과, 앞서 언급한 유틸리티들의 개발을 더 쉽게 만들어주는
관련 도구들이 포함되어 있습니다. 이것은 더 이상 공식적으로 지원되지 않는 특정 게임 시대를 보존하기
위해 스스로에게 취미용 네트워크 서비스를 제공하려는 사람을 위한 완전한 생태계가 되는 것을 목표로 합니다.

바이너리 네트워크 포맷에 대한 훌륭한 설명글을 써주신 Tau님께 감사드립니다.
파이썬 RC4 코드를 짜주신 스택 오버플로우의 어떤 익명의 이용자분께 감사드립니다.
파이썬용 샘플 스니퍼 코드를 짜주신 스택 오버플로우의 또 다른 익명의 이용자분께 감사드립니다.
제 초기 결과물과 비교해볼 수 있도록 easerver에 훌륭한 로그를 남겨주신 Tau님께 다시 한번 감사드립니다.
격려해주시고 진행 상황에 큰 관심을 보여주신 PKGINGO님께 감사드립니다.
여러 게임에서 좋은 리버스 엔지니어링(RE) 파트너가 되어주고 좋은 발견들을 공유해준 Sarah와 Alice에게 감사드립니다.
게임 리버스 엔지니어링을 도와주고 매일 밤 제 피드에 빌어먹을 귀여운 애니메이션 아가씨들을 리트윗해준 helvetica에게 감사드립니다.

## 2dxutils

`.2dx` 오디오 컨테이너 파일의 압축을 풀거나 다시 압축하기 위한 유틸리티입니다. 기존 `.2dx` 파일에서
RIFF WAV 오디오를 추출하거나, 기존 파일을 업데이트하거나, 주어진 WAV 파일들을 사용하여 처음부터
새로운 파일을 생성할 수 있습니다. 이 유틸리티가 최고는 아니며, 시중에 더 완전하고 정확한 프로그램들이
더 있다고 생각합니다. 하지만 제가 알기로는 모두 소스 코드가 공개되어 있지 않아 이 프로그램을 직접 개발했습니다.
사용법을 확인하려면 `./2dxutils --help`를 실행하여 도움말 출력을 확인하십시오.

## afputils

다양한 게임에서 사용되는 여러 애니메이션 포맷을 다루기 위한 유틸리티입니다. 이 유틸리티에는
TXP2 컨테이너 파서 및 리패커, GE2D 도형 파서, AFP/BSI 파서가 포함되어 있습니다. 이들 도구는
AFP와 관련된 작업을 지원하며, AFP는 다양한 게임에서 애니메이션을 처리하기 위해 SWF를 기반으로 만들어진 포크입니다.
이 유틸리티는 IFS 및 TXP2 파일로부터 애니메이션을 렌더링할 수 있으며, 많은 애니메이션 파일에
포함된 Flash 유사 바이트코드를 디컴파일한 의사코드를 제공할 수도 있습니다. 또한 TXP2 컨테이너를 압축 해제하고
새로운 텍스처 파일로 다시 패킹하는 기능도 지원합니다. 이 포맷은 SWF 기반이므로 매우 복잡합니다.
따라서 이 도구들이 모든 게임의 모든 애니메이션을 완벽히 처리할 수 있을 것이라고 기대하긴 어렵습니다.
사용 방법을 확인하려면 ./afputils --help 명령어를 실행하세요.

## api

이 저장소의 BEMAPI 구현의 개발 버전입니다. 이 도구는 점수, 프로필, 라이벌의 네트워크 간 연동을 위한
REST 유사 API 계층 역할을 합니다. 사용법을 확인하려면 `./api --help` 명령어를 실행하세요.
"services" 및 "frontend"와 마찬가지로, 이 도구는 MySQL 데이터베이스 연결 정보와 지원되는 게임 시리즈 정보를
담고 있는 개발용 서비스 설정 파일을 지정해줘야 합니다. 설정 파일 예시는 `config/server.yaml`에서 확인하고
수정할 수 있습니다. 이 유틸리티는 프로덕션 환경에서 사용해서는 안 됩니다. 대신, `bemani/wsgi/api.wsgi` 파일을
참고하세요. 이 파일은 Python 가상 환경, 프로젝트 종속성, uWSGI, nginx와 함께 사용할 수 있도록 준비된
WSGI 파일입니다. 네트워크 연동 기능이 필요 없다면, 이 서비스는 아예 생략해도 괜찮습니다.

## arcutils

`.arc` 파일을 압축 해제하기 위한 유틸리티입니다. 현재는 파일을 다시 패킹하는 기능은 제공하지 않지만,
포맷이 매우 단순하기 때문에 해당 기능을 추가하는 것은 비교적 쉬울 것입니다. 사용 방법을 확인하려면
`./arcutils --help` 명령어를 실행하세요.

## assetparse

특정 게임의 에셋 디렉터리를 가져와 프론트엔드에서 사용할 수 있도록 파일을 변환하는 유틸리티입니다.
이 유틸리티를 사용하면 프론트엔드에서 커스터마이징 미리보기 같은 기능을 활성화할 수 있습니다.
"read"와 마찬가지로, 변환된 에셋을 저장할 올바른 위치를 지정하는 설정 파일이 필요하며, 프론트엔드와
이 유틸리티가 해당 경로를 참조하도록 설정되어야 합니다. 설정 파일 예시는 `config/server.yaml`에서
확인하고 수정할 수 있습니다. "read"와는 달리 이 유틸리티는 필수는 아닙니다. 하지만 실행 중인 게임의
에셋을 변환하지 않으면 프론트엔드에서 미리보기 그래픽을 볼 수 없습니다. 사용 방법을 확인하려면
`./assetparse --help` 명령어를 실행하세요.

## bemanishark

eAmuse 패킷을 디코딩하고 출력할 수 있는 와이어 스니퍼입니다. eAmusement 서버와 지원되는 게임 사이의
트래픽을 감청할 수 있는 컴퓨터에서 실행하면, 요청과 응답을 "services" 로그에서 볼 수 있는 것과
동일한 형식의 XML로 출력합니다. 이 도구는 바이너리 및 XML 트래픽 모두에서 작동합니다. 단, SSL로
암호화된 트래픽은 감청할 수 없기 때문에, 공식 지원이 있는 아케이드에서 이 도구를 실행하려고 해도
작동하지 않습니다. `sudo ./bemanishark`처럼 실행하면 됩니다. 종료될 때까지 무한히 실행되며,
Ctrl-C로 종료할 수 있습니다. 옵션을 보려면 `./bemanishark --help`처럼 실행하세요. 옵션 없이
실행하면 모든 주소에 대해 포트 80을 감청하려고 시도합니다. SN1과 SN2에서 사용되는 Base64 이진
blob 포맷은 지원하지 않습니다. 또한 시간이 지남에 따라 패킷을 잃기 시작할 수 있습니다.
이는 해결하지 못한 버그로, 운영체제가 일부 패킷을 전달하지 않아 TCP 스트림을 재조립하는 데
실패하는 현상으로 보입니다. 이 유틸리티는 독립 실행형 감청 도구보다는 Wireshark용 플러그인으로
다시 작성하는 것이 더 나을 수 있지만, 그럴 시간이 없습니다.

## binutils

A utility for unpacking raw binxml data (files that use the same encoding scheme
as the binary network protocol) to their XML representation. This is useful for
examining raw binary blobs or digging into unknown file formats that contain binxml.
Run it like `./binutils --help` to see help and learn how to use this.

## bootstrap

A utility for quickly bootstrapping a local setup's music database from an already
running BEMAPI-compatible server that has been set up for federation. This is better
documented in the below "Database Initialization" section. Note that this utility assumes
no omnimix support and will bootstrap only normal game databases. The BEMAPI federation
protocol does support omnimix, so if you are bootstrapping against a running instance
that has omnimix databases and you wish to support omnimixes as well, you can look at
the source to this and manually run commands for the games in question.

## cardconvert

A command-line utility for converting between card numbers written on the back of a
card and the card ID stored in the RFID of the card. Run it like `./cardconvert --help`
to see how to use this. This will sanitize input, so you can feed it card numbers
with or without spaces, and you can mix up 1 and I as well as 0 and O, and it will
properly handle decoding. This supports both new and old style e-Amusement cards but
does not support the cross-play network cards with five groups of digits on the back
of the card.

## dbutils

A command-line utility for working with the DB used by "api", "services" and "frontend".
This utility includes options for creating tables in a newly-created DB, granting and
revoking admin rights to the frontend, generating migration scripts for production DBs,
and upgrading production DBs based on previously created migration scripts. Its driven
by alembic under the hood. You will use `create` on initial setup to generate a working
MySQL database. If you change the schema in code, you can use this again with the `generate`
option to generate a migration script. Whenever you run an upgrade to your production
instance, you should run this against your production DB with the `upgrade` option to
bring your production DB up to sync with the code you are deploying. Run it like
`./dbutils --help` to see all options. The config file that this works on is the same
that is given to "api", "services" and "frontend".

## formatfiles

A simple wrapper frontend to black, the formatter used on this project. Running this will
auto-format all of the python code that might need formatting, leaving the rest out. When
submitting pull requests make sure to run this so that your code conforms to the style
used by this project! Run this like `./formatfiles` to fix up all files in the repository.

## frontend

Development version of a frontend server allowing for account and server administration
as well as score viewing and profile editing. Run it like `./frontend --help` to see
help output and determine how to use this. Much like "services" and "api", this should
be pointed at the development version of your services config file which holds
information about the MySQL database that this should connect to as well as what game
series are supported. See `config/server.yaml` for an example file that you can modify.

Do not use this utility to serve production traffic. Instead, see
`bemani/wsgi/api.wsgi` for a ready-to-go WSGI file that can be used with a Python
virtualenv containing this project and its dependencies, uWSGI and nginx. Note thati
this shares a config file with "services" and "api" but is independent, sharing state
with them using the production DB only.

## ifsutils

A mediocre utility that can extract `.ifs` files. This has a lot of baked in
assumptions and is not nearly as good as other open-source utilities for extracting
files. It also cannot repack files yet. This is included for posterity, and because
some bootstrapping code requires it in order to fully start a production server.
Run it like `./ifsutils --help` to see help output and learn how to use it.

## iidxutils

A utility for patching IIDX music database files. Note that this currently can only
apply a "hide leggendarias from normal folders" patch, although it would be trivial
to extend for other uses such as song renames, difficulty patches and other fixups.
Run it like `./iidxutils --help` to see help output and learn how to use it.

## jsx

A utility which takes the existing JSX files in the repository and compiles them to
raw JS files for you. This is offered purely as a way to serve JSX files in a
production setup from nginx or similar instead of compiling them on-the-fly when
they are requested. You can use this to lower cold-start load times of your frontend.
If you do not make use of this or you are running the developent version of "frontend"
then JSX files are compiled on-the-fly when they are requested by the browser. This
behavior makes fast iteration possible by treating JSX files the same way that the
"frontend" debug utility treats python source files but removes the ability for a
production webserver such as nginx to serve static files. Run it like `./jsx --help`
to see help output and learn how to use it.

## proxy

A utility to MITM a network session. Point a game at the port this listens on, and
point this at another network to see the packets flowing between the two. Takes care
of rewriting the facility message to MITM all messages. Has the ability to rewrite
a request/response on the fly which is not currently used except for facility rewriting.
Its possible that this could be used to on-the-fly patch packets coming back from a
network which you don't control to do things such as enable paseli and adjust other
settings that you cannot normally access. Logs in an identical format to "bemanishark".
Useful for black-box RE of other networks. Note that this does not have the ability
to MITM SSL-encrypted traffic, so don't bother trying to use this on an official
network.

This also has the ability to route a packet to one of several known networks based on
the PCBID, so this can also be used as a proxy for switching networks on the fly.
With a config file, this can be used as a HTTP VIP of sorts, allowing you to point all of
your games at a single server that runs this proxy and forward games on a per-PCBID
basis to various networks behind the scenes. This can come in especially handy if you
are serving traffic from the same network your games are on. The network will auto-detect
the public-facing IP of games when they connect and use that info for matching support.
This breaks for local connections, so you might want to set up an offsite proxy instance
so that the correct public-facing IP is detected. For an example config file to use "proxy"
as a VIP, see `config/proxy.yaml`. For a more reliable proxy, use the wsgi version
of this utility located at `bemani/wsgi/proxy.wsgi` along with uWSGI and nginx.

Run it like `./proxy --help` to see how to use this utility.

## psmap

A utility to take an offset from a DLL/EXE file pointing at a psmap structure and
produce python code that would generate a suitable response that said DLL/EXE will
properly parse. Essentially, if you are reversing a new game and they use the `psmap`
function to decode all or part of a packet, you can grab either the physical offset
into the DLL or the virtual address of the data and use this utility to generate
the code necessary to service that request. Note that some psmap structures are
dynamically generated at runtime. "psmap" supports this by emulating x86 and x64 code
to reconstruct the final structure. This feature can be optionally enabled if needed.
Run it like `./psmap --help` to see how to use this utility.

## read

A utility to read music DB information out of game files and populate a database.
This should be given the same config file as "api", "services" or "frontend" and
assumes that "dbutils" has already been used to instantiate a valid MySQL DB. It
also assumes you have the correct game files to read out of. Run it like
`./read --help` to see how to use it. This utility's uses are extensively documented
below in the "Installation" section.

## replay

A utility to take a packet as logged by "proxy", "services", "trafficgen" or
"bemanishark", and replay that packet against a particular server. Useful for
quickly grabbing packets that caused a crash and debugging the crash (and verifying
the fix). It is also compatible with the packet logs found on exception and unsupported
packet messages in the Admin Event Logs page on the frontend. It also lets you
replay that packet against your production instance once you fix the issue in case
that packet was a score or profile update that you care about. Run it like
`./replay --help` to see all information and usage.

## responsegen

A utility to take a packet as logged by "proxy", "services", "trafficgen" or
"bemanishark", and generate python code that would have generated that exact packet.
Useful for quickly grabbing packets sniffed from another network and prototyping new
game support. Think of this as a combination of "replay" and "psmap". This is also
extremely useful when building new integration test clients. Run it like
`./responsegen --help` to see all information and usage.

## sampleclient

A very barebones sample client for the BEMAPI implementation contained in this repo.
Run it like `./sampleclient --help` to see help output and determine how to use this.
Essentially, this is provided as a barebones client that does nothing other than
print fetched info to the screen. You can use this as a starting point for an
application that uses BEMAPI to fetch info from an "api" instance or to test your
production installation to make sure it is ready for federation.

## scheduler

A command-line utility for kicking off scheduled work that must be performed against the
DB. This includes picking new dailies/weeklies, new courses, and others depending on the
game and any requirements that the server perform some actual calculation based on
time. Essentially, any game backend that includes a `run_scheduled_work` override will
be acted on by this utility. Note that this takes care of scheduling cadence and
should be seen as a utility-specific cron handler. You can safely run this repeatedly
and as frequently as desired. Run like `./scheduler --help` to see how to ues this.
This should be given the same config file as "api", "frontend" and "services".

## services

Development version of an eAmusement protocol server using flask and the protocol
libraries also used in "bemanishark" and "trafficgen". Currently it lets most modern
BEMANI games boot and supports full scores, profile and events for Beatmania IIDX 20-26,
Pop'n Music 19-27, Jubeat Saucer, Saucer Fulfill, Prop, Qubell, Clan and Festo, Sound
Voltex 1, 2, 3 Season 1/2 and 4, Dance Dance Revolution X2, X3, 2013, 2014 and Ace,
MÚSECA 1, MÚSECA 1+1/2, MÚSECA Plus, Reflec Beat, Limelight, Colette, groovin'!! Upper,
Volzza 1 and Volzza 2, Metal Gear Arcade, and finally The\*BishiBashi. Note that it also
has matching support for all Reflec Beat versions as well as MGA. By default, this serves
traffic based solely on the database it is configured against. If you federate with
other networks using the "Data API" admin page, it will upgrade to serving traffic
based on the profiles, scores and statistics of all connected networks as well as the
local database. Run like `./services --help` to see how to use this.

Do not use this utility to serve production traffic. Instead, see
`bemani/wsgi/api.wsgi` for a ready-to-go WSGI file that can be used with a Python
virtualenv containing this project and its dependencies, uWSGI and nginx.

## shell

A convenience wrapper to invoke a Python 3 shell that has paths set up to import the
modules in this repository. If you want to tinker or write a quick one-off, this is
probably the easiest way to do so. Run this like `./shell` to drop into a Python REPL
which has the paths set up for correct imports.

## struct

A convenience utility for helping reverse-engineer structures out of game DLLs/EXEs.
You can give this a physical DLL offset or a virtual memory address for the start and
end of the data as well as a python struct format (documentation at
https://docs.python.org/3.8/library/struct.html) and this will print the decoded
data to the screen one entry per line. It includes several enhancements for decoding
pointers to sub-structures and pointers to C strings. Note that much like "psmap", this
has the ability to print out structures that are dynamically constructed at runtime by
emulating x86 and x64 instructions. Run it like `./struct --help` to see how to use this.

## tdxtfiles

Utilities for working with raw TDXT texture files. These are found packed inside TXP2
and TEXP containers but sometimes can be found standalone. This utility has the capability
to extract a PNG of the texture for all known texture formats that I've come across, and
can repack a TDXT file given a PNG of the same size under certain circumstances. Not all
texture formats are supported for repacking. Run it like `./tdxtutils --help` to see help
output and determine how to use it.

## trafficgen

A utility for simulating traffic to an eAmusement service. Given a particular game,
this will run through and attempt to verify simple operation of that service. No
guarantees are made on the accuracy of the emulation though I've strived to be
correct. In some cases, I will verify the response, and in other cases I will
simply verify that certain things exist so as not to crash a real client. This
currently generates traffic emulating Beatmania IIDX 20-26, Pop'n Music 19-27, Jubeat
Saucer, Fulfill, Prop, Qubell, Clan and Festo, Sound Voltex 1, 2, 3 Season 1/2 and 4,
Dance Dance Revolution X2, X3, 2013, 2014 and Ace, The\*BishiBashi, MÚSECA 1 and MÚSECA
1+1/2, Reflec Beat, Reflec Beat Limelight, Reflec Beat Colette, groovin'!! Upper,
Volzza 1 and Volzza 2 ad Metal Gear Arcade and can verify card events and score events
as well as PASELI transactions. Run it like `./trafficgen --help` to see how to use this.
Note tha this takes a config file which sets up how the clients behave. See
`config/trafficgen.yaml` for a sample file that can be used.

## verifylibs

Unit test frontend utility. This will invoke nosetests on the embarrasingly small
collection of unit tests for this repository. If you are making modifications, it can
be useful to write a test first (placed in the `bemani/tests/` directory) and code
from there. It is also useful when optimizing or profiling, and also to verify that
you haven't regressed anything. Supports all options that nosetests does including
filtering, verbose printing and such. Run it like `./verifylibs --help` to see how
to do these things. When submitting pull requests make sure to run this across all
tests by running `./verifylibs` so you know that all tests pass.

## verifylint

Lint invocation utility. This simply invokes flake8 with various options so that you
can see you haven't introduced any lint errors. When submitting pull requests make sure
to run this so you know you aren't introducing any lint errors into the codebase. Run
it like `./verifylint` to print out any lint warnings your modifications have caused.

## verifytraffic

A utility which attempts to call "trafficgen" for each supported game on the network.
Think of this as a full integration test suite, as it will sweep through each supported
game and verify that network services are actually working. This assumes that you are
running "services". Do not point this at a production instance since it **will**
submit bogus cards, scores, names and the like and mess up your network. This takes
a config file which sets up how the client should behave. See `config/trafficgen.yaml`
for a sample file that can be used. When submitting pull requests make sure to run
this against a development version of your server so you know you haven't broken any
existing game implementations.

## verifytyping

Type-checking invocation utility. Since this repository is fully typed, this verifies
that you haven't introduced any type errors and often catches bugs far faster than
attemping to play a round only to see that you misused a class or misspelled a variable.
When submitting pull requests make sure to run this like `./verifytyping` so you know
you aren't introducing any type errors into the codebase.

# 설치 방법

---

## 의존성 설치


이 코드들은 Python 3.8을 기본으로 가정하고 작성되었지만, 이후 버전의 Python에서도 작동해야 합니다.
시스템의 기본 Python으로 Python 3.8을 설치하고 싶지 않거나 설치하지 않은 경우, `virtualenv`를 사용하여
가상 환경을 만드는 것이 권장됩니다. 설치의 나머지 과정은 Python 3.8이 제대로 작동하고 있다고 가정하며
(가상 환경을 사용하는 경우 해당 환경이 활성화되어 있다고 가정합니다). 더 최신 버전의 Python이 있다면,
이 코드는 그와도 호환되어야 합니다.
이 코드는 Linux에서 실행되도록 설계되었습니다. 그러나 시스템 종속적인 라이브러리를 사용하지 않고,
필요한 모든 요소를 순수 Python으로 구현했기 때문에 Windows와 OSX에서도 성공적으로 테스트되었습니다.
다만, 이 전체 도구 모음은 Debian 기반 배포판을 사용해 빌드되고 테스트되었으며, 몇몇 핵심적인 코드 조각은
훨씬 더 빠른 Cython 구현을 포함하고 있기 때문에 이 부분은 사용자의 환경에 따라 결과가 다를 수 있습니다 (YMMV).

필요한 라이브러리를 설치하려면, 저장소의 루트 디렉터리에서 다음 명령어를 실행하세요. 이 명령어를 실행하면
모든 프로그램이 최소한 시작은 가능해집니다. 그러나 대부분의 프로그램을 유용하게 사용하려면 MySQL 데이터베이스가
반드시 필요합니다.
이 단계는 MySQL 서버와 클라이언트, 그리고 MySQL 클라이언트 개발 라이브러리가 설치되어 있어야 수행할 수 있습니다.
또한, `wheel` Python 패키지가 이미 설치되어 있다고 가정합니다. MySQL 클라이언트 라이브러리를 컴파일하려면
시스템에 `libssl` 및 `libcrypto`도 있어야 합니다.
Debian 기반 배포판에서 위 의존성을 충족하려면 아래 명령어를 실행하세요:

```
sudo apt install libssl-dev zlib1g-dev mysql-server mysql-client libmysqlclient-dev
```

위의 모든 요소가 준비되었다면, 다음 명령어를 실행하세요:

```
pip install -r requirements.txt
```

MySQL 설치는 이 README의 범위를 벗어나므로, 새로운 데이터베이스 및 테이블을 생성할 수 있는 권한이 있는
MySQL 데이터베이스가 이미 준비되어 있다고 가정합니다. 이 소프트웨어는 MySQL 버전 5.7 이상이 필요합니다.
이는 5.7에서 추가된 "json" 컬럼 타입을 광범위하게 사용하기 때문입니다. 데이터베이스를 하나 생성하세요
(이 코드의 기본 데이터베이스 이름은 'bemani'입니다). 해당 데이터베이스는 어떤 사용자와 비밀번호를 통해
접근됩니다 (이 코드의 기본 사용자/비밀번호는 'bemani'/'bemani'입니다). 설치에 필요한 모든 테이블을
생성하려면, 아래 명령어를 실행하세요. 단, 설정 파일을 수정한 경우에는 자신이 커스터마이징한 설정 파일로
대체해야 합니다. 여기서 사용하는 설정 파일은 "api", "services", "frontend" 및 위에서 설명된 다양한
유틸리티에서도 동일하게 사용해야 합니다.

```
./dbutils --config config/server.yaml create
```

프런트엔드를 실행하려면 Python이 자바스크립트 런타임을 찾아야 합니다. 이는 렌더링 시점에 리액트 컴포넌트를
미리 컴파일할 수 있으므로 프런트엔드 개발 시 컴파일 단계가 필요 없습니다. 백엔드는 즉시 다시 로드할 수 있지만
해석된 JS 코드를 생성하기 위해 전체 빌드 프로세스를 거쳐야 한다는 점이 정말 마음에 들지 않아서 대신 독립형
서비스 방식을 선택했습니다. JS 런타임을 설치하는 것도 이 문서의 범위를 벗어나는 것이지만, 빠르게 시작할 수
있는 방법은 node.js를 설치하는 것입니다.

기본 구성은 프론트엔드/백엔드 캐시를 `/tmp`로 가리킵니다. 프로덕션 환경에서 파일 시스템 캐시를 사용하여
실행하려는 경우 `/tmp`를 사용하면 일부 항목이 캐시되지 않을 수 있으므로 다른 디렉토리로 변경하는 것이
좋습니다. 이는 Linux의 `/tmp`가 파일 액세스를 작성자만 제한하는 방식 때문에 다른 사용자로 실행되는 여러
유틸리티와 캐시를 공유하면 캐시 재사용에 실패하고 프런트엔드 속도가 크게 느려집니다. 또는 파일 시스템 캐시를
사용하는 대신 멤캐시드 서버를 설정하고 프로덕션 인스턴스가 이를 가리키도록 할 수 있습니다.

## 데이터베이스 초기화

이 시점에서 네트워크를 지정하면 게임이 실행되지만 점수를 저장할 수 없습니다. 이는 노래/차트 -> 점수 매핑이
없기 때문입니다. 트래픽 생성기와 서비스 백엔드의 기본 구성 파일은 config/ 디렉토리에서 찾을 수 있습니다.
데이터베이스 설정을 사용자 정의한 경우 구성 파일에서 호스트명/사용자 이름/비밀번호/데이터베이스를 업데이트해야
합니다. 또한 서버 주소와 프런트엔드 URL도 업데이트하여 인스턴스를 맞춤 설정할 수 있습니다.

곡/차트 -> 점수 매핑을 생성하려면 다음 섹션을 통해 각 게임 시리즈의 데이터를 가져와야 합니다. 사용자 정의한
경우 기본값 대신 사용자 자신의 서비스 구성을 사용해야 합니다. 처음 가져온 이후 파일에 업데이트가 있었다면,
`--update` 플래그를 사용하여 실행할 수 있습니다. 이 플래그는 메타데이터가 건너뛰는 대신 DB에 덮어쓰도록
강제합니다. 일반적으로 이런 일은 발생하지 않지만, 음악 DB 파싱을 개선했다면 데이터베이스를 업데이트하기 위해
이 작업을 수행해야 합니다. 재사용되는 곡 항목이 많이 보일 것입니다. 이는 가져오기 스크립트가 다른 게임
버전에서 동일한 곡에 대한 기존 차트 세트를 찾고 두 게임 버전을 연결할 때 발생합니다. 이것이 동일한 게임의
다른 버전 간에 점수를 공유할 수 있는 방법입니다. 이미 BEMAPI 호환 서버의 승인된 클라이언트인 경우,
원격 서버를 가리키고 기존 데이터베이스를 사용하여 자신의 서버를 시드함으로써 서버 초기화를 빠르게 진행할 수
있습니다. 이 경우 다음 명령을 실행하여 완전한 초기화를 수행하십시오. "bootstrap" 스크립트에는 옴니믹스
버전이 아닌 항목만 있습니다. 옴니믹스 지원을 제공하고 옴니믹스 지원도 있는 다른 BEMAPI 호환 인스턴스를
가리키는 경우 옴니믹스 버전을 추가하도록 편집할 수 있습니다. 새로운 지원 게임이 출시되어 초기 설정을 최신
데이터로 업데이트하려는 경우, 다음 스크립트를 실행하고 `--update` 플래그를 추가할 수 있습니다.
그렇지 않으면 다음과 같이 다음 명령을 실행하십시오.

```
./bootstrap --config config/server.yaml --server http://some-server.here/ --token some-token-here
```

기존 BEMAPI 호환 서버와 연동하지 않는 경우, 실행하려는 게임의 게임 파일에서 서버를 초기화할 수 있습니다.
정확히 어떻게 하는지는 다음 섹션을 참조하십시오.

### Pop'n Music

For Pop'n Music, get the game DLL from the version of the game you want to import and
run a command like so. This network supports versions 19-27 so you will want to run this
command once for every version, giving the correct DLL file. Note that there are several
versions of each game floating around and the "read" script attempts to support as many
as it can but you might encounter a version of the game which hasn't been mapped yet.

An example is as follows:

```
./read --config config/server.yaml --series pnm --version 22 --bin popn22.dll
```

If you are looking to support omnimix v2, you can add songs out of an XML like this:

```
./read --config config/server.yaml --series pnm --version omni-24 --bin popn24.dll --xml your_songs_db.xml
```

If you have more than one XML you want to add, you can run this command with a folder with all your XML files:

```
./read --config config/server.yaml --series pnm --version omni-24 --bin popn24.dll --folder my/xmls/path
```

### Jubeat

For Jubeat, get the music XML out of the data directory of the mix you are importing,
and then use "read" with `--series jubeat` and `--version` corresponding to the following
table:

* Saucer:         saucer
* Saucer Fulfill: saucer-fulfill
* Prop:           prop
* Qubell:         qubell
* Clan:           clan
* Festo:          festo

An example is as follows:

```
./read --config config/server.yaml --series jubeat --version saucer --xml music_info.xml
```

You will also want to populate the Jubeat name database with the following command
after importing all mixes:

```
./read --config config/server.yaml --series jubeat --version all --tsv data/jubeat.tsv
```

For Jubeat Prop and later versions, you will also need to import the emblem DB, or emblems
will not work properly. An example is as follows:

```
./read --config config/server.yaml --series jubeat --version prop \
      --xml data/emblem-info/emblem-info.xml
```

If you wish to display emblem graphics on the frontend, you will also need to convert the
emblem assets. Failing to do so will disable the emblem graphics rendering feature for the
frontend. Note that this only applies to versions where you have also imported the emblem
DB. An example is as follows:

```
./assetparse --config config/server.yaml --series jubeat --version prop \
      --xml data/emblem-info/emblem-info.xml --assets data/emblem-textures/
```

### IIDX

For IIDX, you will need the data directory of the mix you wish to support. The import
script automatically scrapes the music DB as well as the song charts to determine
difficulty, notecounts and BPM. For a normal mix, you will want to run the command like
so. This network supports versions 20-26 so you will want to run this command once for
every version, giving the correct bin file:

```
./read --config config/server.yaml --series iidx --version 22 --bin \
      gamedata/data/info/music_data.bin --assets gamedata/data/sound/
```

Note that for omnimix mixes, you will need to point at the omnimix version of
`music_data.bin`, normally named `music_omni.bin`. For the version, prepend "omni-" to the
number, like so:

```
./read --config config/server.yaml --series iidx --version omni-22 --bin \
      gamedata/data/info/music_omni.bin --assets gamedata/data/sound/
```

You will also want to update the IIDX name database with the following command
after importing all mixes (this fixes some inconsistencies in names):

```
./read --config config/server.yaml --series iidx --version all --tsv \
      data/iidx.tsv
```

For Qpro editing to work properly, you will also need to import the Qpro database from
the mix you wish to support. This does not need to be run separately for omnimix versions,
the base version Qpros will be used for both that version and the omnimix of that version.
This network supports editing Qpros for versions 20-26 so you will want to run this command
once for every version, giving the correct DLL file:

```
./read --config config/server.yaml --series iidx --version 22 --bin bm2dx.dll
```

### DDR

For DDR, you will need the game DLL and `musicdb.xml` from the game you wish to import,
and then run a command similar to the following. You will want to use the version
corresponding to version in the following table:

* X2:            12
* X3 vs. 2ndMix: 13
* 2013:          14
* 2014:          15
* Ace:           16

```
./read --config config/server.yaml --series ddr --version 15 --bin ddr.dll --xml data/musicdb.xml
```

For DDR Ace, there is no `musicdb.xml` or game DLL needed. Instead, you will need the
`startup.arc` file, like the following example:

```
./read --config config/server.yaml --series ddr --version 16 --bin data/arc/startup.arc
```

### SDVX

For SDVX, you will need the game DLL and `music_db.xml` from the game you wish to import,
and then run the following command, modifying the version parameter as required.
Note that for SDVX 1, you want the `music_db.xml` file in `data/others/music_db/` directory,
but for SDVX 2 and onward, you will want the file in `data/others/` instead.

```
./read --config config/server.yaml --series sdvx --version 1 \
      --xml data/others/music_db.xml
```

For SDVX 1, you will also need to import the item DB, or appeal cards will not work
properly. To do so, run the following command.

```
./read --config config/server.yaml --series sdvx --version 1 \
      --bin soundvoltex.dll
```

For SDVX 2 and 3, you will also need to import the appeal message DB, or appeal cards
will not work properly. To do so, run the following command, substituting the correct
version number.

```
./read --config config/server.yaml --series sdvx --version 2 \
      --csv data/others/appealmessage.csv
```

For SDVX 4, you will also need to import the appeal card DB, or appeal cards will not
work properly. To do so, run the following command.

```
./read --config config/server.yaml --series sdvx --version 4 \
      --xml data/others/appeal_card.xml
```

### MÚSECA

For MÚSECA, you will need the `music-info.xml` file from the game you wish to import.
Then, run the following command, modifying the version parameter as required.

```
./read --config config/server.yaml --series museca --version 1 \
      --xml data/museca/xml/music-info.xml
```

### Reflec Beat

For Reflec Beat, get the game DLL from the version of the game you want to import and
run a command like so. This network supports Reflec Beat up through Volzza 2, so you
will want to run this with versions 1-6 to completely initialize. Use the version
corresponding to version in the following table:

* Reflec Beat: 1
* Limelight: 2
* Colette: 3
* Groovin'!!: 4
* VOLZZA: 5
* VOLZZA 2: 6

```
./read --config config/server.yaml --series reflec --version 1 --bin reflecbeat.dll
```

## Running Locally

Once you've set all of this up, you can start the network in debug mode using a command
similar to:

```
./services --port 5730 --config config/server.yaml
```

You can start the frontend in debug mode using another similar command as such:

```
./frontend --port 8573 --config config/server.yaml
```

You can start the BEMAPI REST server in debug mode using a command similar to:

```
./api --port 18573 --config config/server.yaml
```

You can run scheduled work to generate dailies and other such things using a command like so:

```
./scheduler --config config/server.yaml
```

The network config for any particular game should look similar to the following, with
the correct hostname or IP filled in for the services URL. No path is necessary. Note
that if you wish to switch between an existing network and one you serve using the
"proxy" utility, you can set up the services URL to include subdirectories as required
by that network. This code does not examine nor care about anything after the initial
slash, so it can be whatever.

```
<network>
    <timeout __type="u32">30000</timeout>
    <sz_xrpc_buf __type="u32">102400</sz_xrpc_buf>
    <ssl __type="bool">0</ssl>
    <services __type="str">http://127.0.0.1:5730/</services>
</network>
```

If you wish to verify the network's operation with some test traffic, feel free to
point the traffic generator at your development network. You should run it similar to
the command below, substituting the correct port to connect to your network and choosing
one of the supported games. If you don't know a supported game, you can use the `--list`
option to print them. If "Success!" is printed after all checks, you're good to go!

```
./trafficgen --config config/trafficgen.yaml --port 5730 --game pnm-22 && echo Success!
```

You will want to set up a cron job or similar scheduling agent to call "scheduler"
on a regular basis. It is recommended to call it every five minutes since there are cache
warming portions for the front-end that expire every 10 minutes. Game code will register
with internal handlers to perform daily/weekly actions which are kicked off by this script.
Note that if you don't want to have this done automatically in your development environment,
you can simply invoke it before testing with a game. An example invocation of the tool is
as follows:

```
./scheduler --config config/server.yaml
```

Once your network is up and running, if you pull new code down, the DB schema may have
changed. For that, use the same DB util script detailed above in the following manner.
This will walk through all migration scripts that you haven't applied and bring your DB
up to spec. It is recommended to create a deploy script that knows how to install dependencies
and install a new version of these utilities to your production virtualenv and then runs the
following script to ensure that your production DB is kept in sync with upstream changes:

```
./dbutils --config config/server.yaml upgrade
```

Since the network provided is player-first, in order to promote an account to administrator
you will have to create an account on a game first. Once you have done that, you can sign
up for the front-end using those credentials (your card and PIN), and then use the dbutils
script to promote yourself to admin, similar to this command:

```
./dbutils --config config/server.yaml add-admin --username <your-name-here>
```

Once you have create an admin account, you can use tools on the frontend to establish
arcades and their owners. Any administrator can check system settings including event
logs, configure news entries, help users recover passwords and change cards and the like.
Arcade owners can choose how paseli is supported on the machines in their arcade, grant
users credits and configure game options such as which events are active.

## Troubleshooting

If you followed the above instructions, the network should "Just Work" for you. However
there are several gotchas and caveats that might not be obvious to a first-time user of
this software. If you run into trouble these troubleshooting steps may help.

### Logs show that games only request the initial services packet. Additional packets are not sent and games do not go online.

The initial services packet is akin to a DNS request. The response tells games where to
go for each service. The values sent by the server are controlled in `config/server.yaml`.
Make sure the domain or IP in the `server.address` config entry is correct for the
computer you're running services on. Make sure that the IP the DNS entry resolves to,
or the literal IP you've typed in this setting is routable from the game's perspective.
Make sure that the port setting in `server.port` is the same as you've specified in your
command line if you are launching the debug program, or the same as your webserver
config if you are setting up a production instance. Make sure that the specified port
is unblocked in any firewall running on the computer you're running services on.

### Games connect to the server, logs show successful exchanges, there are no exceptions and the game boots fine but freezes on the attract screen or refuses to mark itself as "online".

Even if 100% of the network packets are responded to correctly, if the game itself can't
ping the keepalive host it will refuse to enable online services. Verifiy the
`server.keepalive` setting in `config/server.yaml` to make sure that it points at a
computer that can be reached by the game. Make sure that that computer has enabled ICMP
replies such as ping. Routers often block ping requests. It is recommended that you leave
this as `127.0.0.1` as it will cause the game to ping itself and get a successful reply.
This removes the usefulness of the network test screen outside of the IP setup but it is
known to work.

### pip install fails to compile MySQL on an ARM-based Mac

It appears that if you are installing this software on an ARM-based OSX machine and you
have installed dependencies using brew, library paths are not correctly set up for MySQL
to find the zstd library. As a result, `pip install -r requirements.txt` will fail with
a cryptic error message including the line `ld: library not found for -lzstd`. The
workaround is to specify the zstd library path manually in the pip install line. Try
running the following (or a variation of the following if you've modified your pip
install line already): `LDFLAGS="-L$(brew --prefix zstd)/lib" pip install -r requirements.txt`.

### JSX files fail to compile, music databases fail to read from game files on Windows

Apparently on Windows, the default encoding is unset for Python in some installations.
This can lead to some incredibly confusing errors as JSX files will fail to compile when
you attempt to load the front-end, and importing music databases from various games will
crash with encoding errors. If you run into this problem, you can set a few environment
variables to fix the issue. Make sure that the following are set:

```
export PYTHONIOENCODING=utf-8
export PYTHONLEGACYWINDOWSSTDIO=utf-8
```

### None of my own games pointing at my self-hosted network can be matched with

This is due to the way routers handle internal connections to their public-facing IP.
Even if you tell your games to connect to the DNS entry or public-facing IP of your
network, the router will handle the request internally. Therefore, all of the games
on your own local network will have their public-facing IP detected wrong. You can
get around this by either hosting your network services off-site, or paying for cheap
colocation somewhere and running a "proxy" instance there. The proxy utility (and its
production wsgi counterpart) know how to forward the detected IP through any number of
proxy hops. Once you have set up an external proxy relay or moved your network services
off-site, your own games will get their public-facing IP detected correctly. Remember
that you should still forward the port assigned to each game on the admin interface.

## Production Setup

As alluded to several times in this README, the recommended way to run a production
instance of this code is to set up uWSGI fronted by nginx. You should SSL-encrypt
the frontend and the API services, and its recommended to use LetsEncrypt for a
free certificate that you can manage easily. There are other ways to run this software
and provide SSL credentials but I have no experience with or advice on them.

The easiest way to get up and running is to install MySQL 5.7, nginx and uWSGI along
with Python 3.8 or higher. Create a directory where the services will live and place
a virtualenv inside it (outside the scope of this document). Then, the wsgi files found
in `bemani/wsgi/` can be placed in the directory, uWSGI pointed at them and nginx set up.
The setup for the top-level package will include all of the frontend templates, so you
can set up a nginx directory to serve the static resources directly by pointing at the
static directory inside your virtualenv. If you use "assetparse" to extract assets or
"jsx" to compile static JS, you'll want to add entries in your nginx config to serve
those as well.

For example configurations, an example install script, and an example script to back
up your MySQL instance, see the `examples/` directory. Note that several files have
sections where you are expected to substitute your own values so please read over them
carefully.

# Contributing

Contributions are welcome! Before submitting a pull request, ensure that your code
is type-hint clean by running `./verifytyping` and ensure that it hasn't broken basic
libraries with `./verifylibs`. Make sure that it is also lint-clean with `./verifylint`.
You should also make sure its formatted correctly by running `./formatfiles`.
If you are changing code related to a particular game, it is required to include a
verification in the form of a game traffic emulator, so that basic functionality can
be verified. To ensure you haven't broken another game with your changes, its recommended
to run the traffic generator against your code with various games. For convenience, you
can run `./verifytraffic --config config/trafficgen.yaml` to run all supported games
against your change. Remember that some games require you to run the scheduler to
generate dailies/weeklies, and if you neglect to run this some of the integration
tests will fail as they require full packet support! If possible, please also write
a unit test for your changes. However, if the unit test is just a tautology and an
integration/traffic test will suit better, then do that instead.

For documentation on how the protocol layer works, see "PROTOCOL". For documentation
on how the eAmusement server is intended to work, see "BACKEND". Inside `bemani/data/`
the various DB model files have comments detailing the intended usage of each of the
tables. For documentation on how the BEMAPI REST API should respond, please see the
BEMAPI specification in `bemani/api/`.

When updating DB schema in the various `bemani/data/` python files, you will most-likely
want to generate a migration for others to use. For that, we've integrated with alembic
in order to provide robust migrations. The same DB utility script detailed above will
create a migration script for you, given a message specifying the operation taking place.
You should run this **after** making the code change to the schema in the relevant
file under `bemani/data/mysql`. Alembic will automatically diff your development MySQL
DB against the schema change you've made and generate an appropriate migration. Sometimes
you will want to augment that migration with addtional data transformations. Various
existing migrations do just that, so have a look at them under
`bemani/data/migrations/versions/`. An example is as follows:

```
./dbutils --config config/server.yaml generate --message "Adding timestamp column to user."
```

Once the script finishes, check out the created migration script to be sure its correct
and then check it in.

# Development Tips

Several core components of this repo have a parallel C++ implementation for massive
speed boosts. Several components are also cythonized to squeeze a bit more speed out of
them as well. This project aims to provide a pure-python implementation of everything so
it is not necessary to run with cythonized or compiled code either in development or
production. However, if you want to benefit from the massive speed bumps provided by
the equivalent implementations you can compile the code in-place for your development
setup. The following will compile all needed libraries assuming you have a working
C++ compiler and cython is set up to run on your computer:

```
python3 setup.py build_ext --inplace
```

If you are modifying files that have an equivalent C++ implementation and it changes
their semantics, make sure to test both paths! If you are modifying code that is
cythonized and you've compiled, make sure to re-run the above command or delete the
compiled `.so` files, otherwise your changes will not show up when you test.

# License and Usage

All of the code in this repository is released under the public domain. No attribution or
releasing of source code is required. No warranty of the code or functionality is implied.
However, open source would not flourish without contributions from users the world across.
Pull requests are therefore appreciated! Please note, however, that the code contained in this
repo is meant to facilitate preservation and personal enjoyment of otherwise lost versions
of various arcade games. Do not attempt to check in anything legally owned by a business
or personal entity including source code, images, siterips, game files or anything
similar. Do not attempt to check in support for games currently being offered for sale
by the original manufacturer or games which have not reached their support end-of-life.

Similarly, while I cannot control what you decide to do with this software, it would be
very, very stupid to attempt to run this in a public arcade or convention, or to attempt
to use this with games that you or another person or business are charging money for. If
you decide to do this anyway, do not advertise association with any of this software in
any form whatsoever. Attempting to use this software for commercial gain or to compete
publicly with official game support goes directly against the stated goals of this software.
