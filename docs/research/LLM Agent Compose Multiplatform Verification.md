# **LLM Agent Verification of Compose Multiplatform Applications: Current State of the Art (March 2026\)**

## **Executive Summary and Architectural Paradigm Shift**

The landscape of autonomous software engineering has undergone a definitive architectural shift by March 2026\. The transition from reactive, syntax-level assistance to proactive, agent-driven verification has fundamentally altered how cross-platform applications are validated. Large Language Model (LLM) agents, operating within local environments such as the Claude Code CLI and terminal multiplexers (CMUX), now demand direct access to application runtimes to execute, observe, interact, and verify state autonomously. This requirement presents unique challenges for Compose Multiplatform (CMP) applications, which eschew native platform view hierarchies in favor of custom-drawn canvases via the Skia graphics engine.

For an autonomous agent to effectively verify a CMP application across iOS, Android, Desktop, and Web targets, it requires either robust computer vision capabilities to interpret raw framebuffers or an intermediate bridge that projects the canvas structure into a semantic, machine-readable accessibility tree. The reliance on raw visual screenshots introduces profound latency and token consumption bottlenecks—often requiring 500KB to 2MB of context per interaction.1 Consequently, as of March 2026, the industry has standardized around the Model Context Protocol (MCP) to bridge this gap, translating platform-specific accessibility APIs into structured JSON that agentic models like Claude Sonnet 4.6 (released February 2026, [https://www.anthropic.com/transparency](https://www.anthropic.com/transparency)) can process with high token efficiency.2

This exhaustive research report investigates the tooling, frameworks, APIs, and community prior art available for LLM-driven verification of Compose Multiplatform applications. Every framework and capability is anchored to its explicit release state as of March 30, 2026\. The analysis systematically assesses headless execution potential, semantic tree exposure, and integration complexity for autonomous CLI-bound agents, culminating in definitive end-to-end workflow recommendations.

## **1\. iOS Simulator Automation for LLM Agents**

The iOS Simulator has historically presented significant barriers to headless, terminal-bound automation due to its tight coupling with the macOS Xcode graphical user interface and the proprietary nature of the Apple ecosystem. However, developments throughout 2025 and early 2026 in both native Apple tooling and open-source MCP wrappers have established viable pathways for CMUX-based LLM agents.

### **Low-Level Simulator Control and Visual Extraction**

The standard Apple binary xcrun simctl remains the foundational tool for simulator lifecycle management. As of Xcode 26.3 (released February 2026), xcrun simctl permits headless booting, URL routing, and screenshot capture via the xcrun simctl io booted screenshot command.4 However, simctl interacts strictly at the framebuffer level; it possesses no inherent capabilities to parse view hierarchies or inject touch coordinates based on semantic element IDs.

To bridge this visual output to an LLM agent, the community relies on lightweight HTTP/WebSocket wrappers. A prominent open-source implementation, simctl-server ([https://gist.github.com/seabass011/d2b00c9f46b71ab656eec5faaad32d1c](https://gist.github.com/seabass011/d2b00c9f46b71ab656eec5faaad32d1c), updated late 2025/early 2026), exposes a /screenshot/{udid}/base64 endpoint.7 This allows an agent to continuously poll visual state, effectively giving the model "eyes" without invoking the DOM or accessibility layers.7 While this raw framebuffer extraction is highly resilient to structural code changes, it consumes immense context window capacity and introduces high latency due to the inference cost of vision models. Furthermore, simctl cannot inject tap or swipe events autonomously, meaning a visual-only approach requires complex coordinate mapping via AppleScript or external tools, severely increasing setup complexity for a Claude Code agent.

### **Appium Support for Compose Multiplatform iOS**

For structural verification, the agent must access the semantic tree. Compose Multiplatform 1.9.3, released on March 26, 2026 ([https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md](https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md)), natively maps its Modifier.semantics properties—such as testTag and contentDescription—directly to the iOS native accessibilityIdentifier and accessibilityLabel.8 This projection makes the custom Skia canvas visible to Apple's Accessibility Services and the XCTest framework.8

Appium remains a primary conduit for extracting this tree. Appium version 3.2.1, released on March 8, 2026 ([https://github.com/appium/appium/releases](https://github.com/appium/appium/releases)), paired with the appium-xcuitest-driver version 10.14.4, provides full support for reading the CMP accessibility tree on iOS.11 Appium's architecture parses the XCTest accessibility dump and returns it via the W3C WebDriver protocol. However, Appium introduces a heavy Node.js dependency and requires the WebDriverAgent (WDA) to be compiled and signed via xcodebuild on the host machine, resulting in a high setup complexity and execution latency for a standalone Claude Code agent.13

### **Semantic Tree APIs and Headless XCTest Execution**

LLM agents can inspect Compose UI elements on the iOS Simulator without Xcode being open by leveraging headless XCTest execution. The xcodebuild test-without-building command allows CLI-bound agents to execute pre-compiled UI tests entirely from the terminal.14 Within these tests, the XCUIApplication().performAccessibilityAudit() API can be invoked to extract the semantic hierarchy projected by Compose.8 While this provides high-fidelity structured data, it forces the LLM to write, compile, and execute Swift/Kotlin test binaries for every interaction, which breaks the dynamic "observe and interact" loop required by autonomous agents.

### **MCP Servers Wrapping iOS Simulator Control**

The most significant advancement for LLM agents in early 2026 is the proliferation of dedicated Model Context Protocol (MCP) servers that wrap iOS automation. The mobile-mcp project (latest version as of March 27, 2026, [https://github.com/mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)) utilizes native WebDriverAgent protocols to extract structured accessibility snapshots.15 This server exposes tools such as mobile\_list\_elements\_on\_screen, which returns UI elements with their respective coordinates and properties as structured JSON.15 By prioritizing structured data over computer vision, mobile-mcp allows the agent to execute deterministic, coordinate-based taps without exhausting token limits.15 Crucially, if the accessibility tree fails to project specific CMP canvas elements, mobile-mcp includes a fallback mechanism that evaluates the raw screen using visual sensing to determine tap coordinates.15

Other specialized servers include the yorifuji-mcp-ios-simulator-screenshot (March 26, 2026), which provides a dedicated channel for streaming xcrun simctl outputs directly into the MCP context window.4

### **Apple and JetBrains Agent Integrations**

In a paradigm-shifting move, Apple introduced the "Claude Agent SDK" natively within Xcode 26.3 on February 3, 2026 ([https://www.anthropic.com/news/apple-xcode-claude-agent-sdk](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)).16 This integration officially supports MCP, allowing external agents to capture SwiftUI and CMP visual Previews and read project structures autonomously without requiring the IDE to be actively manipulated by a human.16 This enables a tight loop where a Claude Code CLI agent can alter Kotlin common code, trigger an iOS Preview headless build, and visually verify the result via Apple's native MCP bridge.16

## **2\. Android Emulator Automation for LLM Agents**

Android's inherently open architecture naturally lends itself to terminal-based automation, making it a highly reliable and performant target for LLM agent verification within a CMUX environment.

### **ADB Screencap and UIAutomator2**

The Android Debug Bridge (adb) facilitates robust screenshot extraction via adb exec-out screencap \-p \> screen.png and basic UI hierarchy dumping via adb shell uiautomator dump.6 Because Compose Multiplatform maps its semantics to Android's native AccessibilityNodeInfo, the UI Automator dump intrinsically contains the required contentDescription and resource-id fields defined in the shared Kotlin code.18

For LLM-agent-driven verification, executing raw ADB commands via the shell is a mature and well-documented approach. However, adb UI dumping is notoriously slow, often taking several seconds per screen, and is prone to XML truncation on highly complex nested Compose layouts. While mature as of March 2026, relying purely on ADB shell scripts limits the velocity of the autonomous verification loop.

### **Emulator gRPC APIs for Programmatic Control**

To bypass the overhead and instability of the ADB daemon, the ecosystem has shifted toward direct remote procedure calls. The Android Emulator exposes a headless gRPC API. The android-emulator Rust crate (version 0.1.0, released February 10, 2026, [https://lib.rs/crates/android-emulator](https://lib.rs/crates/android-emulator)) provides full programmatic bindings to the Android Emulator gRPC controller API.20

This interface permits an LLM agent to programmatically list, configure, and spawn headless emulator instances (EmulatorConfig::new().with\_window(false)) directly from the CLI.20 It supports injecting precise touch events, rotation mapping, and hardware keystrokes via gRPC, entirely eliminating ADB latency.20 For a Claude Code agent, executing Rust binaries or Python gRPC scripts to control the emulator state is vastly superior to screen-scraping, representing a mature and headless-capable integration path.

### **Maestro on Compose Multiplatform Android**

Maestro has evolved into the definitive declarative testing tool. As of March 2026, Maestro fully supports Compose Multiplatform Android applications.21 Maestro inherently reads the Android accessibility tree, matching the semantics projected by the CMP runtime.23 Maestro is completely CLI-driven, allowing a CMUX agent to execute flows via shell commands like maestro test flow.yaml.

More importantly, Maestro bundles its own native MCP server (maestro mcp), which can be invoked directly from the Claude Code CLI.24 This server allows the AI to discover YAML flows, execute them headlessly, retrieve detailed HTML/XML execution trails, and dynamically query the UI state without needing to parse raw UIAutomator XML.24

### **Android Studio Gemini Integration**

Google's release of Android Studio Meerkat in early 2026 heavily focuses on agentic workflows, featuring a headless Gemini CLI ([https://geminicli.com/docs/get-started/authentication/](https://geminicli.com/docs/get-started/authentication/)) capable of interacting with the project environment.27 The Gemini integration includes Agent Mode, which can build apps, parse crashes, and generate UI code.30

However, evaluating this for external verification reveals severe limitations. The Gemini integration is tightly bound to the Android Studio process or its proprietary CLI. It does not expose standard semantic trees to third-party clients like Claude Code. Therefore, while Android Studio Meerkat can verify Compose UI internally, it cannot effectively serve as a headless verification engine driven by an external Claude Code CLI agent from outside the IDE ecosystem.

### **Headless Execution of Compose UI Test**

The Kotlin testing library, compose-test, can be executed headlessly on an emulator by an LLM agent. By utilizing the command ./gradlew :composeApp:connectedAndroidTest in the terminal, the agent triggers the Gradle instrumentation runner against a background emulator.14 The test interacts with the semantic tree using standard matchers (e.g., onNodeWithTag("button").performClick()).14 While highly reliable, this requires the agent to write and compile test code rather than dynamically inspecting the live view, making it better suited for final regression validation rather than exploratory verification.

## **3\. Compose for Web as a Verification Proxy**

Given the immense computational overhead and fragility of managing virtual mobile devices within a CMUX environment, leveraging the web target of Compose Multiplatform as a rapid verification proxy has emerged as a highly effective strategy for LLM agents.

### **Stability and Feature Parity of Compose for Web**

As of Compose Multiplatform 1.9.3 (released March 26, 2026, [https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html](https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html)), the Web target built on Kotlin/Wasm has officially reached Beta stability, indicating a high degree of production readiness.32 The legacy Kotlin/JS target remains Stable.32

Feature parity between the Web target and iOS/Android is remarkably comprehensive in 2026\. The 1.9.3 release includes full support for Material 3 Expressive themes, customizable shadows, and the new context menu API across all web targets.33 A critical enhancement in CMP 1.9.3 is the introduction of the WebElementView() composable, which allows for seamless integration of native HTML elements into the Compose canvas, improving interoperability.33

However, known divergences persist. Web targets do not perfectly replicate mobile hardware constraints (e.g., camera APIs, Bluetooth), and typography rendering can differ subtly between the browser's engine and mobile Skia implementations.23 Furthermore, accessibility support for interop container views utilizing complex scrolls and sliders is currently unavailable on the web target.33

### **Playwright MCP and Accessibility Tree Interaction**

Prior to CMP 1.9.3, the Compose Web canvas was a black box to standard Document Object Model (DOM) inspectors, rendering web automation tools effectively blind. Crucially for agent verification, CMP 1.9.3 introduces initial accessibility support for web targets, enabled by default.33 The framework now projects its semantic properties (role, contentDescription, stateDescription) directly into the browser's native accessibility tree.33

Because of this projection, standard web automation scripts using Playwright or Puppeteer can reliably interact with the Compose for Web canvas. The @playwright/mcp server ([https://playwright.dev/docs/accessibility-testing](https://playwright.dev/docs/accessibility-testing)) has become the definitive tool for LLM web automation in 2026\.1 The Playwright MCP server operates strictly on the accessibility tree rather than relying on computer vision.37 It extracts the page state as a structured hierarchy of roles, names, and states—consuming a mere 2 to 5 Kilobytes of token context, compared to the 500KB to 2MB required to process a raw screenshot.1

This architectural alignment allows the Claude Code CLI to launch a headless Chromium browser, navigate to the local Compose Web development server, and execute deterministic interactions (click, fill) based purely on the semantic tree.37

### **Web as a Proxy Strategy**

Using the Web target as a verification proxy is a highly reasonable and resource-efficient strategy for the vast majority of application categories. For business logic verification, state management, navigation flows, and form validation, the web proxy provides sub-second latency and minimal token consumption.33 However, for applications heavily reliant on native mobile sensors, precise gesture physics (like iOS scroll inertia), or platform-specific UI bindings (like Apple Pay), the agent must still rely on the Android Emulator or iOS Simulator for final validation.

## **4\. JetBrains Tooling for LLM Agents and Compose Multiplatform**

The JetBrains ecosystem underwent a massive realignment in late 2025 and early 2026, pivoting aggressively away from traditional remote desktop paradigms toward multi-agent orchestration protocols.

### **The Sunset of JetBrains Fleet**

The experimental lightweight IDE, JetBrains Fleet, which heavily promoted remote development capabilities, was officially deprecated. JetBrains announced the cessation of all updates and distribution for Fleet, effective December 22, 2025 ([https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/](https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/)).39 Consequently, any architectural plans to utilize Fleet's programmatic API access or remote development bridges for running and inspecting Compose apps via external LLM agents are obsolete. The engineering resources were reallocated to focus exclusively on agentic development environments.

### **JetBrains Central and the Agent Client Protocol (ACP)**

Replacing Fleet's conceptual space is JetBrains Central, officially announced on March 24, 2026 ([https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/)).42 JetBrains Central acts as a control and execution plane designed to orchestrate agent-driven software production across IDEs, CLIs, and continuous integration pipelines.42

To facilitate interoperability with external agents like Claude Code, JetBrains formalized the Agent Client Protocol (ACP).43 ACP allows an external LLM agent running in a terminal to hook directly into the IntelliJ IDE backend, effectively exposing the IDE's semantic code analysis, refactoring engines, and internal MCP servers as modular tools to the CLI agent.44

Within JetBrains IDEs (like IntelliJ IDEA 2026.1 and Android Studio), the JetBrains AI Assistant natively supports ACP-compatible agents. The IDE settings expose an integrated MCP server that can be passed directly to installed agents.44 This means a Claude Code agent running in CMUX can leverage JetBrains' advanced codebase indexing to locate Compose Multiplatform UI components and verify compiler states without parsing the raw AST manually.

### **KotlinConf 2025 and Roadmap Announcements**

At KotlinConf 2025, JetBrains open-sourced Koog, a JVM-native framework specifically designed for building AI agents in Kotlin.45 This framework allows development teams to build custom agent logic that deeply understands Kotlin idioms and Compose state paradigms. Furthermore, the stabilization of Compose Multiplatform for iOS and the transition to the K2 compiler as the default in IntelliJ IDEA 2025.1 were major milestones that provided the necessary compiler speed and API stability for agent-driven iterative development.45 The roadmap for 2026 emphasizes "Agentic Software Development" as the primary focus, indicating that APIs for IDE-level operations will only expand throughout the year.42

## **5\. Cross-Platform UI Testing Frameworks Compatible with LLM Agents**

LLM agents require execution environments that are resilient to flakiness, provide deterministic inputs, and are capable of deep platform inspection. The testing framework landscape in 2026 offers several distinct approaches.

### **Maestro (Version 2.2.0)**

Maestro ([https://maestro.dev/](https://maestro.dev/)) has solidified its position as the premier framework for LLM-driven Compose Multiplatform testing. Version 2.2.0, released in early March 2026, natively supports Compose Multiplatform across iOS, Android, and Web targets.21 Maestro inherently interacts with the accessibility tree across all platforms, matching the exact semantics projected by the CMP runtime without relying on brittle DOM selectors or XPath.23

Maestro's architecture is uniquely suited for LLM agents. Test flows are defined in declarative YAML, which an LLM can effortlessly generate, read, and modify.26 For example, a flow can instruct the framework to tapOn: "Submit" or assertVisible: "Welcome". Furthermore, Maestro bundles its own native MCP server (maestro mcp), which can be invoked directly from the Claude Code CLI.24 This integration allows the AI assistant to dynamically discover Maestro flows, understand test structures, suggest improvements, and execute the tests headlessly against local emulators.24 The execution speed is significantly faster than Appium, seamlessly handling the timing and synchronization issues inherent in mobile automation, making it highly reliable for autonomous loops.13

### **Agent-Device CLI**

A notable community advancement specifically designed for LLM-agent-driven mobile UI testing is the agent-device framework developed by Callstack in 2026 ([https://www.callstack.com/blog/agent-device-ai-native-mobile-automation-for-ios-android](https://www.callstack.com/blog/agent-device-ai-native-mobile-automation-for-ios-android)).51 Operating as a lightweight CLI and daemon stack, agent-device exposes token-efficient primitives like open, snapshot, click, scroll, and type directly to the agent.51

Instead of generating a massive XML dump, agent-device extracts highly compressed, structured accessibility tree snapshots that fit cleanly within the context limits of models like Claude Sonnet 4.6.51 It bridges exploratory agent actions with deterministic replay by recording .ad scripts, allowing an agent to explore a Compose app dynamically and then codify the successful path into a repeatable regression test.51

### **Kaspresso and Detox**

Kaspresso (latest 1.x-SNAPSHOT, 2026\) offers deep Compose integration and declarative Kotlin DSL wrappers.52 While it executes extremely quickly and provides robust built-in protection against flaky tests, it remains strictly Android-bound, relying heavily on Espresso and UI Automator.52 Its lack of iOS support severely limits its utility for a unified Compose Multiplatform agent workflow.

Detox ([https://github.com/wix/Detox](https://github.com/wix/Detox)) relies on gray-box, in-process synchronization to eliminate timing-based flakiness.53 While highly effective and stable for React Native applications, it explicitly lacks support for native Compose Multiplatform compilation targets, rendering it unusable for verifying CMP apps.50

## **6\. Computer Use and Visual AI Approaches**

When semantic tree extraction fails due to incomplete Modifier.semantics coverage, or when visual regression testing is explicitly required, agents must fall back to visual processing paradigms.

### **Anthropic Computer Use API**

Anthropic's Computer Use API (beta version computer-use-2025-01-24), utilizing the Claude Sonnet 4.6 model, allows the LLM to directly observe and manipulate graphical desktop interfaces.2 By running the iOS Simulator and Android Emulator in standard windowed modes on a macOS host, the Computer Use API can calculate precise pixel coordinates and inject global mouse and keyboard events directly into the operating system.16

This approach completely bypasses platform-specific automation frameworks and accessibility bridges, making it universally applicable regardless of the underlying UI technology. However, it is highly susceptible to OS-level interruptions, screen resolution scaling disparities, and consumes substantial token bandwidth per interaction (upwards of 100,000 tokens for complex screens).58 Relying purely on this API for a continuous verify-fix loop is economically and temporally expensive.

### **MacOS Native Accessibility (AXUIElement)**

To optimize local macOS automation and reduce reliance on expensive vision models, researchers and open-source developers have leveraged Apple's native AXUIElement APIs. Tools like Screen2AX (July 2025, [https://arxiv.org/html/2507.16704v1](https://arxiv.org/html/2507.16704v1)) and macos-visual-agent ([https://github.com/peakmojo/macos-visual-agent](https://github.com/peakmojo/macos-visual-agent)) extract the real-time hierarchical accessibility metadata of the entire macOS desktop—including the internal contents of the active iOS Simulator window—translating it into a structured tree.59

Screen2AX achieves a 77% F1 score in reconstructing complete accessibility trees from desktop environments, allowing an agent to interact with the simulator window semantically without invoking xcrun simctl or compiling WebDriverAgent.61 This acts as a hybrid "virtual display" approach, projecting the simulator's pixels into a semantic desktop structure that the LLM can parse efficiently.

### **Screenshot-Based Verification and Precedents**

Screenshot-based verification remains a critical fallback. Maestro 2.2.0 introduced the assertScreenshot command, allowing for visual regression testing by cropping screenshots to specific elements and comparing against reference images.49 Additionally, the simctl-server mentioned previously provides a direct pipeline for base64 PNG extraction.7 While tooling is mature, the precedent established in 2025–2026 is that screenshot verification should be reserved strictly for visual layout validation (e.g., "does this button render correctly in dark mode?"), while functional interaction should strictly utilize semantic trees to prevent action-level hallucinations and token exhaustion.23

## **7\. Community Solutions and Prior Art**

The developer community has actively discussed and documented end-to-end workflows for AI-driven mobile UI verification throughout late 2025 and 2026\.

Discussions on platforms like Reddit and community forums highlight the shift away from brittle DOM selectors toward structured semantic approaches. For example, engineers utilizing Playwright MCP note that constraining AI interactions to a fixed set of tools based on the accessibility tree drastically reduces hallucinations and makes automation deterministic.37

Open-source projects combining LLMs with mobile simulators are proliferating. The mobile-mcp (Mobile Next) project is widely recognized as a robust solution for enabling platform-agnostic interaction across native iOS and Android apps without distinct platform knowledge.15 Similarly, the agent-device stack by Callstack provides a clear precedent for building a token-efficient, token-aware automation loop designed explicitly for coding assistants.51

In JetBrains and Kotlin community forums, discussions frequently revolve around the maturity of Compose Multiplatform. A consensus has formed that the stabilization of iOS in 2025 and the Beta status of Wasm in 2026 have removed the primary blockers for widespread enterprise adoption, leading to a surge in demand for cross-platform automated testing strategies.64

## **Quantitative Tool Assessment and Metrics**

The following structured matrix defines the capabilities of the primary tools evaluated for Claude Code CLI integration as of March 30, 2026, satisfying the specific assessment criteria requested.

| Tool / Framework | Version Status (Mar 2026\) | Headless Execution (No GUI) | Tree Exposure | Estimated Setup Complexity (Claude Code CLI) |
| :---- | :---- | :---- | :---- | :---- |
| **Maestro** | 2.2.0 (March 2026\) 49 | Yes (CLI/Cloud) 24 | Semantic (Native AX) | **Low** \- Bundled native MCP server; YAML declarative.25 |
| **Playwright MCP** | Latest (2026) 1 | Yes (Headless Browser) | Semantic (DOM AX) | **Low** \- NPM package; native integration with CLI.1 |
| **mobile-mcp** | Latest (2026) 15 | Requires running Emulator/Sim | Semantic \+ Visual Fallback | **Low/Medium** \- NPM package, standardizes iOS/Android JSON.15 |
| **agent-device** | Latest (2026) 51 | Requires running Emulator/Sim | Semantic | **Medium** \- Requires daemon configuration and custom scripting.51 |
| **Appium (XCUITest)** | 3.2.1 (March 2026\) 11 | Requires running Simulator | Semantic | **High** \- Requires Xcode WDA compilation, Node.js overhead.13 |
| **android-emulator** | 0.1.0 (Feb 2026\) 20 | Yes (gRPC headless spawn) 20 | N/A (Lifecycle only) | **Medium** \- Rust binary integration.20 |
| **simctl-server** | Latest (2026) 7 | Requires running Simulator | Visual Only (Base64) | **Low** \- Python script, simple API.7 |
| **Appium (Windows)** | ⚠️ \[Pre-2022 source — unmaintained\]67 | Requires Windows VM | Semantic | **High** \- Deprecated and brittle execution.67 |

## **Final Deliverables and Strategic Recommendations**

Based on the exhaustive analysis of the ecosystem as of March 30, 2026, the following workflows and conclusions are provided for an autonomous LLM agent tasked with verifying Compose Multiplatform applications.

### **Most Promising End-to-End Workflow Recommendations per Platform**

* **Web Target:** Utilize **Playwright MCP**. The agent runs a local Vite/Webpack server, launches a headless Chromium instance, and interacts with the CMP 1.9.3 accessibility tree via the MCP bridge. This is the fastest, lowest-latency, and most token-efficient method for verifying shared business logic and Compose UI state.33  
* **Android Target:** Utilize **Maestro 2.2.0 via MCP**. The agent spawns a headless emulator using the android-emulator gRPC Rust crate.20 It then invokes the maestro mcp tool to dynamically query the Android accessibility tree, generate YAML test flows, and execute them to verify platform-specific integrations.24  
* **iOS Target:** Utilize the **Apple Claude Agent SDK** (if running inside Xcode 26.3) 16 or **mobile-mcp** (if running externally in CMUX). The agent boots a simulator via xcrun simctl. It uses mobile-mcp's mobile\_list\_elements\_on\_screen tool to parse the XCTest semantic tree mapped by CMP, performing coordinate-based taps and relying on visual fallback only when the accessibility tree is truncated.15  
* **Desktop Target (macOS):** Utilize **Screen2AX** combined with Anthropic Computer Use APIs. Because dedicated testing frameworks for CMP Desktop are lacking, the agent must extract the macOS AXUIElement tree via Screen2AX to locate the window coordinates, followed by programmatic mouse clicks via the Computer Use API.56

### **Identified Gaps: Platforms with No Good Solution**

A severe gap persists in **Desktop (macOS/Windows/Linux) CMP Automation**. While Compose for Desktop is Stable 32, testing frameworks like Maestro, agent-device, and mobile-mcp explicitly target mobile and web. Appium's Mac2 and Windows drivers are notoriously brittle, and the Microsoft WinAppDriver has been explicitly unmaintained since 2022 ⚠️ \[Pre-2025 source — verify current status\].67 Consequently, agents verifying Desktop targets are forced into high-token-cost visual or OS-level accessibility paradigms, lacking the streamlined YAML abstractions available on mobile. Furthermore, the death of JetBrains Fleet 39 removes a potential avenue for streamlined remote API inspection.

### **Top Overall Approaches for Cross-Platform Agents**

1. **The Web Proxy Strategy (Primary Loop):** Execute 80% of the exploratory verify-fix loop against the CMP Web (Wasm) target using Playwright MCP. The feature parity is high enough that logical errors, navigation issues, and layout bugs can be squashed without the immense overhead of mobile emulators.1  
2. **Maestro MCP Integration (Validation Loop):** For final validation on mobile targets, rely entirely on Maestro 2.2.0's bundled MCP server. It abstracts away the timing flakiness of mobile platforms and works seamlessly across both iOS and Android without requiring the agent to understand distinct platform internals.23

### **Surprising and Non-Obvious Findings**

* **Token Economics Dictate Architecture:** The push toward MCP servers like mobile-mcp and Playwright MCP is not just about convenience; it is driven by LLM token economics. Extracting a structured JSON accessibility tree costs \~2KB of context, while evaluating a raw screenshot costs up to 2MB.1 An autonomous loop using screenshots will rapidly hit context limits and accrue massive API costs, rendering raw visual verification viable only as a secondary fallback.  
* **Visual Fallback as a Necessity:** Despite improvements in CMP 1.9.3, the Skia canvas does not always project complex, deeply nested semantic trees perfectly to the host OS. The most effective MCP servers (mobile-mcp) explicitly include computer vision fallbacks to calculate tap coordinates when the semantic tree fails, highlighting the necessity of hybrid approaches.15  
* **The Death of Fleet Changes IDE Integration:** The abrupt cancellation of JetBrains Fleet in December 2025 forces agents to rely on JetBrains Central and the Agent Client Protocol (ACP) hooking into heavier IDEs like IntelliJ IDEA, fundamentally changing how agents will interface with project structures programmatically.39

#### **Works cited**

1. Playwright MCP Changes the Build vs. Buy Equation for AI Testing in 2026 | Bug0, accessed March 30, 2026, [https://bug0.com/blog/playwright-mcp-changes-ai-testing-2026](https://bug0.com/blog/playwright-mcp-changes-ai-testing-2026)  
2. Anthropic's Transparency Hub, accessed March 30, 2026, [https://www.anthropic.com/transparency](https://www.anthropic.com/transparency)  
3. awesome-mcp-servers/README.md at main \- GitHub, accessed March 30, 2026, [https://github.com/punkpeye/awesome-mcp-servers/blob/main/README.md](https://github.com/punkpeye/awesome-mcp-servers/blob/main/README.md)  
4. MCP iOS Simulator Screenshot \- LobeHub, accessed March 30, 2026, [https://lobehub.com/mcp/yorifuji-mcp-ios-simulator-screenshot](https://lobehub.com/mcp/yorifuji-mcp-ios-simulator-screenshot)  
5. Tools I Love: xcrun simctl io booted recordVideo · Blog \- Eli Perkins, accessed March 30, 2026, [https://blog.eliperkins.com/tools-i-love-xcrun-simctl-recordVideo/](https://blog.eliperkins.com/tools-i-love-xcrun-simctl-recordVideo/)  
6. Is there a way to have an AI Agent see the emulator screen so it can iterate? \- Reddit, accessed March 30, 2026, [https://www.reddit.com/r/FlutterDev/comments/1nnxox7/is\_there\_a\_way\_to\_have\_an\_ai\_agent\_see\_the/](https://www.reddit.com/r/FlutterDev/comments/1nnxox7/is_there_a_way_to_have_an_ai_agent_see_the/)  
7. iOS Simulator Bridge for AI Agents \- gives agents eyes into mobile screens \- GitHub Gist, accessed March 30, 2026, [https://gist.github.com/seabass011/d2b00c9f46b71ab656eec5faaad32d1c](https://gist.github.com/seabass011/d2b00c9f46b71ab656eec5faaad32d1c)  
8. Support for iOS accessibility features | Kotlin Multiplatform Documentation, accessed March 30, 2026, [https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html](https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html)  
9. Compose kmp IOS \- Issues/Bugs \- Appium Discuss, accessed March 30, 2026, [https://discuss.appium.io/t/compose-kmp-ios/45724](https://discuss.appium.io/t/compose-kmp-ios/45724)  
10. compose-multiplatform/CHANGELOG.md at master \- GitHub, accessed March 30, 2026, [https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md](https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md)  
11. Appium Versions \- Sauce Labs Documentation, accessed March 30, 2026, [https://docs.saucelabs.com/mobile-apps/automated-testing/appium/appium-versions/](https://docs.saucelabs.com/mobile-apps/automated-testing/appium/appium-versions/)  
12. Releases · appium/appium \- GitHub, accessed March 30, 2026, [https://github.com/appium/appium/releases](https://github.com/appium/appium/releases)  
13. Mobile Automation Testing in 2026: The Complete Strategy Guide, accessed March 30, 2026, [https://contextqa.com/blog/mobile-testing-strategy-that-actually-works-2026/](https://contextqa.com/blog/mobile-testing-strategy-that-actually-works-2026/)  
14. Testing Compose Multiplatform UI \- Kotlin, accessed March 30, 2026, [https://kotlinlang.org/docs/multiplatform/compose-test.html](https://kotlinlang.org/docs/multiplatform/compose-test.html)  
15. mobile-next/mobile-mcp: Model Context Protocol Server for ... \- GitHub, accessed March 30, 2026, [https://github.com/mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)  
16. Apple's Xcode now supports the Claude Agent SDK \- Anthropic, accessed March 30, 2026, [https://www.anthropic.com/news/apple-xcode-claude-agent-sdk](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)  
17. Apple added native Claude Agent support to Xcode and this is bigger than it looks \- Reddit, accessed March 30, 2026, [https://www.reddit.com/r/ClaudeCode/comments/1qvn8g6/apple\_added\_native\_claude\_agent\_support\_to\_xcode/](https://www.reddit.com/r/ClaudeCode/comments/1qvn8g6/apple_added_native_claude_agent_support_to_xcode/)  
18. Semantics | Jetpack Compose \- Android Developers, accessed March 30, 2026, [https://developer.android.com/develop/ui/compose/accessibility/semantics](https://developer.android.com/develop/ui/compose/accessibility/semantics)  
19. Accessibility in Jetpack Compose \- Android Developers, accessed March 30, 2026, [https://developer.android.com/develop/ui/compose/accessibility](https://developer.android.com/develop/ui/compose/accessibility)  
20. Android Emulator gRPC Control Library \- Lib.rs, accessed March 30, 2026, [https://lib.rs/crates/android-emulator](https://lib.rs/crates/android-emulator)  
21. Maestro, End-to-End UI Testing for Mobile and Web, accessed March 30, 2026, [https://maestro.dev/](https://maestro.dev/)  
22. Top 5 E2E Testing Frameworks in 2026: Ranked & Compared \- Maestro, accessed March 30, 2026, [https://maestro.dev/insights/top-5-end-to-end-testing-frameworks-compared](https://maestro.dev/insights/top-5-end-to-end-testing-frameworks-compared)  
23. Best Mobile UI Testing Tools in 2026: Drizz vs Appium vs Maestro, accessed March 30, 2026, [https://www.drizz.dev/post/mobile-ui-testing-platforms-2026](https://www.drizz.dev/post/mobile-ui-testing-platforms-2026)  
24. Maestro CLI commands and options, accessed March 30, 2026, [https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options](https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options)  
25. Maestro: A single framework for mobile and web E2E testing | The Dennis Blog, accessed March 30, 2026, [https://www.dennis-whalen.com/post/maestro/](https://www.dennis-whalen.com/post/maestro/)  
26. Maestro: Empowering Teams to Ship Mobile Apps with Confidence | by Jan Rabe | Medium, accessed March 30, 2026, [https://medium.com/@kibotu/maestro-empowering-teams-to-ship-mobile-apps-with-confidence-577ecb43f55e](https://medium.com/@kibotu/maestro-empowering-teams-to-ship-mobile-apps-with-confidence-577ecb43f55e)  
27. Gemini CLI authentication setup, accessed March 30, 2026, [https://geminicli.com/docs/get-started/authentication/](https://geminicli.com/docs/get-started/authentication/)  
28. Android Studio Meerkat Feature Drop | 2024.3.2 (May 2025), accessed March 30, 2026, [https://developer.android.com/studio/releases/past-releases/as-meerkat-feature-drop-release-notes](https://developer.android.com/studio/releases/past-releases/as-meerkat-feature-drop-release-notes)  
29. Android Studio Meerkat | 2024.3.1 (March 2025), accessed March 30, 2026, [https://developer.android.com/studio/releases/past-releases/as-meerkat-release-notes](https://developer.android.com/studio/releases/past-releases/as-meerkat-release-notes)  
30. Android Developer fireside chat: Talking about Gemini in Android Studio \- YouTube, accessed March 30, 2026, [https://www.youtube.com/watch?v=9caMeFQYCLk](https://www.youtube.com/watch?v=9caMeFQYCLk)  
31. Gemini in Android Studio features, accessed March 30, 2026, [https://developer.android.com/studio/gemini/features](https://developer.android.com/studio/gemini/features)  
32. Stability of supported platforms | Kotlin Multiplatform Documentation, accessed March 30, 2026, [https://kotlinlang.org/docs/multiplatform/supported-platforms.html](https://kotlinlang.org/docs/multiplatform/supported-platforms.html)  
33. What's new in Compose Multiplatform 1.9.3 \- Kotlin, accessed March 30, 2026, [https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html](https://kotlinlang.org/docs/multiplatform/whats-new-compose-190.html)  
34. What's new in Kotlin 2.2.20, accessed March 30, 2026, [https://kotlinlang.org/docs/whatsnew2220.html](https://kotlinlang.org/docs/whatsnew2220.html)  
35. Accessibility | Kotlin Multiplatform Documentation, accessed March 30, 2026, [https://kotlinlang.org/docs/multiplatform/compose-accessibility.html](https://kotlinlang.org/docs/multiplatform/compose-accessibility.html)  
36. Accessibility testing \- Playwright, accessed March 30, 2026, [https://playwright.dev/docs/accessibility-testing](https://playwright.dev/docs/accessibility-testing)  
37. State of Playwright AI Ecosystem in 2026 \- Currents, accessed March 30, 2026, [https://currents.dev/posts/state-of-playwright-ai-ecosystem-in-2026](https://currents.dev/posts/state-of-playwright-ai-ecosystem-in-2026)  
38. What is the Accessibility Tree? How Playwright, Cypress, and Selenium Use It Differently, accessed March 30, 2026, [https://testdino.com/blog/accessibility-tree/](https://testdino.com/blog/accessibility-tree/)  
39. The Future of Fleet \- The JetBrains Blog, accessed March 30, 2026, [https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/](https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/)  
40. JetBrains Fleet dropped for AI products instead : r/programming \- Reddit, accessed March 30, 2026, [https://www.reddit.com/r/programming/comments/1pnz3n0/jetbrains\_fleet\_dropped\_for\_ai\_products\_instead/](https://www.reddit.com/r/programming/comments/1pnz3n0/jetbrains_fleet_dropped_for_ai_products_instead/)  
41. JetBrains discontinues Fleet IDE \- InfoWorld, accessed March 30, 2026, [https://www.infoworld.com/article/4104991/jetbrains-discontinues-fleet-ide.html](https://www.infoworld.com/article/4104991/jetbrains-discontinues-fleet-ide.html)  
42. Introducing JetBrains Central: An Open System for Agentic Software Development, accessed March 30, 2026, [https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/)  
43. Agent Client Protocol (ACP): Use Any Coding Agent in Any IDE \- JetBrains, accessed March 30, 2026, [https://www.jetbrains.com/acp/](https://www.jetbrains.com/acp/)  
44. Agent Client Protocol (ACP) | AI Assistant Documentation \- JetBrains, accessed March 30, 2026, [https://www.jetbrains.com/help/ai-assistant/acp.html](https://www.jetbrains.com/help/ai-assistant/acp.html)  
45. KotlinConf 2025 Unpacked: Upcoming Language Features, AI-Powered Development, and Kotlin Multiplatform Upgrades \- The JetBrains Blog, accessed March 30, 2026, [https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/](https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/)  
46. KotlinConf 2026, May 20–22, Munich, accessed March 30, 2026, [https://kotlinconf.com/](https://kotlinconf.com/)  
47. JetBrains AI | Intelligent Coding Assistance, AI Solutions, and More, accessed March 30, 2026, [https://www.jetbrains.com/ai/](https://www.jetbrains.com/ai/)  
48. JetBrains reveals Kotlin 2.2, Amper, AI tools at KotlinConf 2025 \- Developer Tech News, accessed March 30, 2026, [https://www.developer-tech.com/news/jetbrains-reveals-kotlin-2-2-amper-ai-tools-at-kotlinconf-2025/](https://www.developer-tech.com/news/jetbrains-reveals-kotlin-2-2-amper-ai-tools-at-kotlinconf-2025/)  
49. Maestro/CHANGELOG.md at main · mobile-dev-inc/Maestro \- GitHub, accessed March 30, 2026, [https://github.com/mobile-dev-inc/maestro/blob/main/CHANGELOG.md](https://github.com/mobile-dev-inc/maestro/blob/main/CHANGELOG.md)  
50. The Best Mobile App Testing Frameworks in 2026 \- Maestro, accessed March 30, 2026, [https://maestro.dev/insights/best-mobile-app-testing-frameworks](https://maestro.dev/insights/best-mobile-app-testing-frameworks)  
51. Agent Device: iOS & Android Automation for AI Agents \- Callstack, accessed March 30, 2026, [https://www.callstack.com/blog/agent-device-ai-native-mobile-automation-for-ios-android](https://www.callstack.com/blog/agent-device-ai-native-mobile-automation-for-ios-android)  
52. KasperskyLab/Kaspresso: Android UI test framework \- GitHub, accessed March 30, 2026, [https://github.com/KasperskyLab/Kaspresso](https://github.com/KasperskyLab/Kaspresso)  
53. The Best Mobile E2E Testing Frameworks in 2026: Strengths, Tradeoffs, and Use Cases, accessed March 30, 2026, [https://www.qawolf.com/blog/best-mobile-app-testing-frameworks-2026](https://www.qawolf.com/blog/best-mobile-app-testing-frameworks-2026)  
54. iOS Automation Testing Tools in 2026: XCUITest, Appium & Beyond | Drizz, accessed March 30, 2026, [https://www.drizz.dev/post/ios-automation-testing-tools-in-2026](https://www.drizz.dev/post/ios-automation-testing-tools-in-2026)  
55. 5 Best Cross Platform Frameworks for App Dev in 2026, accessed March 30, 2026, [https://platform.uno/articles/best-cross-platform-frameworks-2026/](https://platform.uno/articles/best-cross-platform-frameworks-2026/)  
56. Anthropic Computer Use API: Desktop Automation Guide \- Digital Applied, accessed March 30, 2026, [https://www.digitalapplied.com/blog/anthropic-computer-use-api-guide](https://www.digitalapplied.com/blog/anthropic-computer-use-api-guide)  
57. LLMs as Scalable, General-Purpose Simulators For Evolving Digital Agent Training \- arXiv, accessed March 30, 2026, [https://arxiv.org/html/2510.14969v1](https://arxiv.org/html/2510.14969v1)  
58. using ax tree for llm web automation hitting context limits need advice : r/LocalLLM \- Reddit, accessed March 30, 2026, [https://www.reddit.com/r/LocalLLM/comments/1rcencg/using\_ax\_tree\_for\_llm\_web\_automation\_hitting/](https://www.reddit.com/r/LocalLLM/comments/1rcencg/using_ax_tree_for_llm_web_automation_hitting/)  
59. AXUIElement.h | Apple Developer Documentation, accessed March 30, 2026, [https://developer.apple.com/documentation/applicationservices/axuielement\_h](https://developer.apple.com/documentation/applicationservices/axuielement_h)  
60. peakmojo/macos-visual-agent: On-device screen understanding for macOS \- GitHub, accessed March 30, 2026, [https://github.com/peakmojo/macos-visual-agent](https://github.com/peakmojo/macos-visual-agent)  
61. Screen2AX: Vision-Based Approach for Automatic macOS Accessibility Generation \- arXiv, accessed March 30, 2026, [https://arxiv.org/html/2507.16704v1](https://arxiv.org/html/2507.16704v1)  
62. Playwright AI Ecosystem 2026: MCP, Agents & Self-Healing Tests | TestDino, accessed March 30, 2026, [https://testdino.com/blog/playwright-ai-ecosystem/](https://testdino.com/blog/playwright-ai-ecosystem/)  
63. Mobile Development MCP Servers, accessed March 30, 2026, [https://mcpmarket.com/categories/mobile-development](https://mcpmarket.com/categories/mobile-development)  
64. How mature is the Compose Multiplatform ecosystem for web development in 2025?, accessed March 30, 2026, [https://www.reddit.com/r/Kotlin/comments/1opdyp4/how\_mature\_is\_the\_compose\_multiplatform\_ecosystem/](https://www.reddit.com/r/Kotlin/comments/1opdyp4/how_mature_is_the_compose_multiplatform_ecosystem/)  
65. Kotlin Multiplatform: 2025 Updates and 2026 Predictions \- Aetherius Solutions, accessed March 30, 2026, [https://www.aetherius-solutions.com/blog-posts/kotlin-multiplatform-in-2026](https://www.aetherius-solutions.com/blog-posts/kotlin-multiplatform-in-2026)  
66. Kotlin Multiplatform Testing in 2025: Complete Guide to Unit, Integration & UI Tests, accessed March 30, 2026, [https://www.kmpship.app/blog/kotlin-multiplatform-testing-guide-2025](https://www.kmpship.app/blog/kotlin-multiplatform-testing-guide-2025)  
67. Appium Drivers \- Appium Documentation, accessed March 30, 2026, [https://appium.io/docs/en/3.2/ecosystem/drivers/](https://appium.io/docs/en/3.2/ecosystem/drivers/)