# 언리얼 엔진 데일리 브리핑 | 2025년 10월 29일

> 최근 7일간 새로운 공식 릴리즈 및 핫픽스 업데이트는 없었습니다. 아래 보고서는 **가장 최신 공식 정보**를 기준으로 작성되었습니다.

---

## 1. 핵심 요약

### 주요 업데이트 상위 3개 (UE 5.7 Preview 기준)

1.  **PCG 프레임워크 정식 버전 (Production-Ready) 전환**
    PCG(Procedural Content Generation Framework)가 정식 버전으로 전환되었으며, 확장성 및 GPU 성능이 크게 향상되었습니다. UE 5.5 대비 약 2배 빨라졌습니다.
    *   출처: Unreal Engine Forum ([https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958](https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958)) | 게시일: 2025-09-23

2.  **Substrate 머티리얼 정식 버전 전환**
    Substrate 머티리얼 시스템이 정식 버전으로 전환되어, 고품질의 물리적 정확도를 가진 복합 재질(예: 금속, 클리어 코트, 피부)을 표현할 수 있게 되었습니다.
    *   출처: Unreal Engine Forum ([https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958](https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958)) | 게시일: 2025-09-23

3.  **MegaLights 베타 버전 전환**
    MegaLights가 베타 버전으로 전환되었으며, 디렉셔널 라이트, Niagara 파티클 라이트, 투명도 라이팅 등을 지원합니다. 해상도 및 업데이트 속도 관리를 위한 성능 튜닝 컨트롤이 추가되었습니다.
    *   출처: Unreal Engine Forum ([https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958](https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958)) | 게시일: 2025-09-23

### 즉시 확인 필요 사항

*   **UE 5.7 Preview: Linux SDL2 → SDL3 전환 예정**
    UE 5.7 정식 버전부터 Linux에서 SDL2가 SDL3로 전환될 예정입니다. SDL2 코드를 커스터마이징한 사용자는 SDL3에 맞게 변경 사항을 재작업해야 합니다.
    *   출처: 5.6.1 Hotfix Released Forum Post ([https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316](https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316)) | 게시일: 2025-08-12

---

## 2. 공식 릴리즈 및 패치

### 버전 릴리즈: Unreal Engine 5.6.1 Hotfix (최신)

*   **버전 번호:** 5.6.1
*   **주요 변경사항:** 270개 이상의 버그 수정 및 업데이트가 포함된 핫픽스입니다. 특히 MetaHuman 관련 버그와 PCG 관련 에디터 크래시 및 이슈 해결에 중점을 두었습니다.
*   **Breaking Changes:** 5.7 버전에서 Linux의 SDL2가 SDL3로 전환될 예정이며, 이는 향후 Breaking Change로 작용할 수 있습니다.
    *   출처: 5.6.1 Hotfix Released Forum Post ([https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316](https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316)) | 게시일: 2025-08-12
*   **릴리즈 노트 URL:** [https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316](https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316)

---

## 3. 버그 및 이슈

> 최근 7일간 Issue Tracker의 주요 업데이트는 확인되지 않았습니다. 아래는 UE 5.6.1 핫픽스에서 수정된 주요 버그 목록입니다.

### 수정된 주요 버그 (UE 5.6.1 Hotfix 기준)

*   **MetaHuman 관련 다수 크래시 및 오류 수정:** MH-15645 (DNA interchange OOM crash), MH-15649 (Crash after failing to load archetype skeletal mesh), MH-15650 (Crash on face sculpting) 등 MetaHuman Creator 에셋 관련 다수의 크래시 및 오류가 수정되었습니다.
*   **PCG 에디터 크래시 수정:** UE-282213 (Editor crash when using PCG self pruning and complex collision) 등 PCG 관련 에디터 안정성 문제가 수정되었습니다.
*   **기타 수정 사항:** UE-290686 (MRQ Quick Render - Selected Cameras No Longer Works with Multiple Cameras), UE-289268 (StateTree Delegate binds to the wrong task) 등 다양한 컴포넌트 및 기능의 버그가 수정되었습니다.
    *   출처: 5.6.1 Hotfix Released Forum Post ([https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316](https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316)) | 게시일: 2025-08-12
*   **Issue Tracker URL:** [https://issues.unrealengine.com/](https://issues.unrealengine.com/)

---

## 4. GitHub 업데이트

> 최근 7일간 EpicGames/UnrealEngine GitHub의 주요 커밋 및 Pull Request는 확인되지 않았습니다.

### 주요 커밋 및 Pull Request (UE 5.6.1 Hotfix 기준)

*   **UE-210136:** Allow Mutable CustomizableObjects to be compiled in -game mode (GitHub 11643)
    Mutable CustomizableObjects가 -game 모드에서 컴파일될 수 있도록 허용하는 커밋이 포함되었습니다.
    *   출처: 5.6.1 Hotfix Released Forum Post ([https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316](https://forums.unrealengine.com/t/5-6-1-hotfix-released/2639316)) | 게시일: 2025-08-12
*   **GitHub URL:** [https://github.com/EpicGames/UnrealEngine](https://github.com/EpicGames/UnrealEngine)

---

## 5. 공식 포럼 기술 논의

### Epic Staff 답변 기술 스레드 (최신)

*   **Unreal Engine 5.7 Preview 발표**
    Epic Games 직원(TinaWisdom)이 UE 5.7 Preview의 주요 신기능과 변경사항을 상세히 발표했습니다. (PCG, Substrate, MegaLights 등)
    *   출처: Unreal Engine Forum ([https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958](https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958)) | 게시일: 2025-09-23
*   **포럼 URL:** [https://forums.unrealengine.com/tags/c/announcements/49/unreal-engine](https://forums.unrealengine.com/tags/c/announcements/49/unreal-engine)

---

## 6. 신기능 및 실험적 기능 (UE 5.7 Preview 기준)

### 새로 추가된 기능 (정식 버전 전환)

*   **PCG 프레임워크 정식 버전 전환 (Production-Ready)**
    GPU 파라미터 오버라이드 및 스케일링 개선을 통해 성능이 향상되었으며, 독립 실행형 그래프 실행 기능이 추가되었습니다.
*   **Substrate 머티리얼 정식 버전 전환**
    Adaptive GBuffer 및 Blendable GBuffer를 지원하며, 여러 재질 레이어를 물리적으로 정확하게 조합할 수 있습니다.

### Beta/Experimental 기능 및 주의사항

*   **실험적 기능: Procedural Vegetation Editor**
    Fab 에셋을 사용하여 Nanite 지원 폴리지(Foliage)를 에디터 내에서 실시간으로 생성, 수정, 커스터마이징할 수 있습니다. PCG 기반 노드 그래프로 구성됩니다.
*   **실험적 기능: Nanite Foliage**
    Nanite Assemblies, Nanite Skinning, Nanite Voxel 시스템을 기반으로 고밀도, 고디테일 폴리지를 60fps로 렌더링 및 애니메이션할 수 있습니다.
*   **베타 기능: MegaLights**
    디렉셔널 라이트, Niagara 파티클 라이트 등을 지원하며, 성능 튜닝 컨트롤이 추가되었습니다.
*   **주의사항: Epic Developer Assistant**
    UI는 미리보기에서 확인 가능하지만, 기능 자체는 5.7 정식 릴리즈와 함께 제공될 예정입니다. (현재는 Epic Developer Community에서 웹 버전 체험 가능)
    *   출처: Unreal Engine Forum ([https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958](https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958)) | 게시일: 2025-09-23

---

## 7. 플러그인 및 문서 업데이트

> 최근 7일간 공식 플러그인 및 문서의 주요 업데이트는 확인되지 않았습니다. 아래는 UE 5.7 Preview의 주요 변경 사항입니다.

### MetaHuman 플러그인 업데이트 (UE 5.7 Preview 기준)

*   **Linux 및 macOS 지원:** MetaHuman Creator 플러그인이 Linux 및 macOS를 지원합니다.
*   **스크립팅 API 추가:** MetaHuman Creator Python 및 Blueprint API를 통해 MetaHuman 캐릭터 에셋의 편집 및 조립 작업을 스크립트로 처리할 수 있습니다.
*   **애니메이션 도구 개선:** 애니메이션 Selection Sets, 간소화된 Animation Mode UI, 통합된 Constraint UX 창 등 애니메이션 워크플로우 개선이 포함되었습니다.
    *   출처: Unreal Engine Forum ([https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958](https://forums.unrealengine.com/t/unreal-engine-5-7-preview/2658958)) | 게시일: 2025-09-23

---

<p style="text-align: center; font-size: 12px; color: #777777; margin-top: 40px;">본 보고서는 언리얼 엔진의 공식 정보를 기반으로 자동 생성되었습니다. 기술적 정확성을 위해 노력하였으나, 최종 작업 전 반드시 공식 문서를 확인하십시오.</p>
