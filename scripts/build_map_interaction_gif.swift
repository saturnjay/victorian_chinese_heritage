#!/usr/bin/env swift

import AppKit
import ImageIO
import UniformTypeIdentifiers

// Rebuild with:
// swift scripts/build_map_interaction_gif.swift

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let screenshotURL = root.appendingPathComponent("proposal/screenshots/03-explorer-map.png")
let photoURL = root.appendingPathComponent("assets/verified-findings/VCH-007-white-hills-cemetery.jpg")
let outputDirectory = root.appendingPathComponent("media", isDirectory: true)
let outputURL = outputDirectory.appendingPathComponent("map-interaction-demo.gif")

guard let screenshot = NSImage(contentsOf: screenshotURL),
      let photo = NSImage(contentsOf: photoURL) else {
  fputs("Missing source screenshot or finding photograph.\n", stderr)
  exit(1)
}

try FileManager.default.createDirectory(at: outputDirectory, withIntermediateDirectories: true)

let width: CGFloat = 1200
let height: CGFloat = 750
let canvas = NSRect(x: 0, y: 0, width: width, height: height)
let sourceSize = screenshot.size
let sx = width / sourceSize.width
let sy = height / sourceSize.height

let ink = NSColor(calibratedRed: 0.105, green: 0.105, blue: 0.09, alpha: 1)
let red = NSColor(calibratedRed: 0.67, green: 0.06, blue: 0.035, alpha: 1)
let green = NSColor(calibratedRed: 0.18, green: 0.43, blue: 0.34, alpha: 1)
let cream = NSColor(calibratedRed: 0.98, green: 0.965, blue: 0.925, alpha: 1)

enum Scene { case opening, chronology, search, focus, detail, route, closing }
struct FrameSpec { let scene: Scene; let progress: CGFloat; let delay: Double }

func ease(_ value: CGFloat) -> CGFloat {
  let t = max(0, min(1, value))
  return t * t * (3 - 2 * t)
}

func roundedRect(_ rect: NSRect, radius: CGFloat, fill: NSColor, stroke: NSColor? = nil, lineWidth: CGFloat = 1) {
  let path = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
  fill.setFill()
  path.fill()
  if let stroke {
    stroke.setStroke()
    path.lineWidth = lineWidth
    path.stroke()
  }
}

func text(_ value: String, in rect: NSRect, size: CGFloat, color: NSColor = ink,
          weight: NSFont.Weight = .regular, alignment: NSTextAlignment = .left) {
  let style = NSMutableParagraphStyle()
  style.alignment = alignment
  style.lineBreakMode = .byWordWrapping
  let attributes: [NSAttributedString.Key: Any] = [
    .font: NSFont.systemFont(ofSize: size, weight: weight),
    .foregroundColor: color,
    .paragraphStyle: style
  ]
  (value as NSString).draw(in: rect, withAttributes: attributes)
}

func label(_ kicker: String, _ title: String, _ body: String, at origin: NSPoint, width boxWidth: CGFloat = 365) {
  let box = NSRect(x: origin.x, y: origin.y, width: boxWidth, height: 104)
  NSGraphicsContext.current?.saveGraphicsState()
  NSShadow().apply {
    $0.shadowColor = NSColor.black.withAlphaComponent(0.18)
    $0.shadowBlurRadius = 18
    $0.shadowOffset = NSSize(width: 0, height: 6)
  }
  roundedRect(box, radius: 17, fill: NSColor.white.withAlphaComponent(0.97))
  NSGraphicsContext.current?.restoreGraphicsState()
  text(kicker.uppercased(), in: NSRect(x: box.minX + 18, y: box.minY + 14, width: box.width - 36, height: 16), size: 10, color: red, weight: .bold)
  text(title, in: NSRect(x: box.minX + 18, y: box.minY + 34, width: box.width - 36, height: 27), size: 18, weight: .bold)
  text(body, in: NSRect(x: box.minX + 18, y: box.minY + 65, width: box.width - 36, height: 28), size: 11.5, color: NSColor.darkGray)
}

extension NSShadow {
  func apply(_ configure: (NSShadow) -> Void) { configure(self); set() }
}

func pulse(at point: NSPoint, progress: CGFloat, color: NSColor = red) {
  let p = ease(progress)
  for index in 0..<2 {
    let local = max(0, min(1, p * 1.35 - CGFloat(index) * 0.28))
    let radius = 18 + local * 35
    let ring = NSBezierPath(ovalIn: NSRect(x: point.x - radius, y: point.y - radius, width: radius * 2, height: radius * 2))
    color.withAlphaComponent((1 - local) * 0.48).setStroke()
    ring.lineWidth = 4
    ring.stroke()
  }
}

func cursor(at point: NSPoint) {
  let path = NSBezierPath()
  path.move(to: point)
  path.line(to: NSPoint(x: point.x + 4, y: point.y + 25))
  path.line(to: NSPoint(x: point.x + 10, y: point.y + 18))
  path.line(to: NSPoint(x: point.x + 16, y: point.y + 30))
  path.line(to: NSPoint(x: point.x + 22, y: point.y + 27))
  path.line(to: NSPoint(x: point.x + 15, y: point.y + 15))
  path.line(to: NSPoint(x: point.x + 25, y: point.y + 14))
  path.close()
  NSColor.white.setFill(); path.fill()
  ink.setStroke(); path.lineWidth = 2; path.stroke()
}

func drawBase(zoom: CGFloat = 1, center: NSPoint = NSPoint(x: 760, y: 420)) {
  let destination: NSRect
  if zoom == 1 {
    destination = canvas
  } else {
    destination = NSRect(
      x: center.x - center.x * zoom,
      y: center.y - center.y * zoom,
      width: width * zoom,
      height: height * zoom
    )
  }
  screenshot.draw(
    in: destination,
    from: NSRect(origin: .zero, size: sourceSize),
    operation: .copy,
    fraction: 1,
    respectFlipped: true,
    hints: [.interpolation: NSImageInterpolation.high]
  )
}

func drawOpening(_ p: CGFloat) {
  drawBase()
  NSColor.black.withAlphaComponent(0.20 * (1 - ease(p))).setFill(); canvas.fill()
  label("Victorian Chinese Heritage Map", "Explore 86 places across Victoria", "Search, filter, move through time, and open the evidence behind each map point.", at: NSPoint(x: 42, y: 600), width: 440)
}

func drawChronology(_ p: CGFloat) {
  drawBase()
  let start = NSPoint(x: 695, y: 570)
  let end = NSPoint(x: 635, y: 44)
  let t = ease(p)
  let point = NSPoint(x: start.x + (end.x - start.x) * t, y: start.y + (end.y - start.y) * t)
  pulse(at: end, progress: p)
  cursor(at: point)
  roundedRect(NSRect(x: 85, y: 14, width: 505, height: 73), radius: 12, fill: NSColor.white.withAlphaComponent(0.96))
  text("1 OF 86 · 1850s", in: NSRect(x: 102, y: 23, width: 470, height: 16), size: 10, color: red, weight: .bold)
  text("Beechworth Chinatown and Chinese camp landscape", in: NSRect(x: 102, y: 42, width: 470, height: 22), size: 15, weight: .bold)
  text("Step through the evidence chronologically", in: NSRect(x: 102, y: 65, width: 470, height: 15), size: 10.5, color: NSColor.darkGray)
}

func drawSearch(_ p: CGFloat) {
  drawBase()
  roundedRect(NSRect(x: 665, y: 19, width: 350, height: 47), radius: 24, fill: .white, stroke: red.withAlphaComponent(0.55), lineWidth: 2)
  text("Bendigo", in: NSRect(x: 701, y: 31, width: 280, height: 24), size: 16, weight: .medium)
  let start = NSPoint(x: 635, y: 44)
  let end = NSPoint(x: 916, y: 43)
  let t = ease(p)
  cursor(at: NSPoint(x: start.x + (end.x - start.x) * t, y: start.y + (end.y - start.y) * t))
  label("Search every field", "Find places, people and evidence", "The results list and visible markers update together.", at: NSPoint(x: 40, y: 604), width: 365)
}

func drawFocus(_ p: CGFloat) {
  let zoom = 1 + ease(p) * 0.42
  drawBase(zoom: zoom, center: NSPoint(x: 750, y: 405))
  let marker = NSPoint(x: 746, y: 428)
  pulse(at: marker, progress: p, color: green)
  cursor(at: NSPoint(x: marker.x + 8, y: marker.y + 8))
  label("Map and index stay connected", "Focus on a heritage cluster", "Select a marker to move from geographic context into the verified place record.", at: NSPoint(x: 42, y: 602), width: 410)
}

func drawDetail(_ p: CGFloat) {
  drawBase(zoom: 1.28, center: NSPoint(x: 755, y: 410))
  NSColor.black.withAlphaComponent(0.18).setFill(); canvas.fill()
  let t = ease(p)
  let panelWidth: CGFloat = 390
  let panelX = width - panelWidth * t
  roundedRect(NSRect(x: panelX, y: 0, width: panelWidth + 20, height: height), radius: 0, fill: cream)
  if t > 0.25 {
    let alpha = min(1, (t - 0.25) / 0.45)
    NSGraphicsContext.current?.saveGraphicsState()
    NSGraphicsContext.current?.compositingOperation = .sourceOver
    photo.draw(in: NSRect(x: panelX + 22, y: 24, width: 346, height: 175), from: .zero, operation: .sourceOver, fraction: alpha, respectFlipped: true, hints: [.interpolation: NSImageInterpolation.high])
    text("WHITE HILLS · BENDIGO", in: NSRect(x: panelX + 24, y: 222, width: 340, height: 17), size: 10, color: red.withAlphaComponent(alpha), weight: .bold)
    text("White Hills Cemetery Chinese section and funerary tower", in: NSRect(x: panelX + 24, y: 247, width: 340, height: 75), size: 22, color: ink.withAlphaComponent(alpha), weight: .bold)
    roundedRect(NSRect(x: panelX + 24, y: 328, width: 93, height: 27), radius: 13, fill: green.withAlphaComponent(0.14 * alpha))
    text("Verified", in: NSRect(x: panelX + 24, y: 334, width: 93, height: 18), size: 11, color: green.withAlphaComponent(alpha), weight: .bold, alignment: .center)
    text("A major Chinese funerary landscape with surviving footstones, unmarked graves and a rare brick tower.", in: NSRect(x: panelX + 24, y: 376, width: 340, height: 82), size: 15, color: ink.withAlphaComponent(alpha))
    text("History  ·  Significance  ·  Evidence  ·  Access  ·  Sources", in: NSRect(x: panelX + 24, y: 478, width: 340, height: 42), size: 12, color: red.withAlphaComponent(alpha), weight: .semibold)
    roundedRect(NSRect(x: panelX + 24, y: 548, width: 340, height: 92), radius: 13, fill: NSColor.white.withAlphaComponent(0.78 * alpha))
    text("VISIT RESPONSIBLY", in: NSRect(x: panelX + 40, y: 565, width: 305, height: 16), size: 10, color: red.withAlphaComponent(alpha), weight: .bold)
    text("Burial place and continuing ritual site. Do not disturb graves or funerary structures.", in: NSRect(x: panelX + 40, y: 588, width: 305, height: 45), size: 12, color: ink.withAlphaComponent(alpha))
    NSGraphicsContext.current?.restoreGraphicsState()
  }
}

func drawRoute(_ p: CGFloat) {
  drawBase()
  let route = [
    NSPoint(x: 436, y: 449), NSPoint(x: 565, y: 500), NSPoint(x: 614, y: 502),
    NSPoint(x: 655, y: 525), NSPoint(x: 700, y: 505), NSPoint(x: 779, y: 510)
  ]
  let line = NSBezierPath(); line.move(to: route[0])
  for point in route.dropFirst() { line.line(to: point) }
  NSColor.white.withAlphaComponent(0.8).setStroke(); line.lineWidth = 8; line.stroke()
  red.withAlphaComponent(0.86).setStroke(); line.lineWidth = 4; line.stroke()
  let segments = route.count - 1
  let scaled = ease(p) * CGFloat(segments)
  let index = min(segments - 1, Int(scaled))
  let local = scaled - CGFloat(index)
  let a = route[index], b = route[index + 1]
  let cursorPoint = NSPoint(x: a.x + (b.x - a.x) * local, y: a.y + (b.y - a.y) * local)
  pulse(at: cursorPoint, progress: p, color: red)
  cursor(at: cursorPoint)
  label("Interpretive journey", "Hover the Walk from Robe route", "Follow the commemorative path into Victoria and open its historical sources.", at: NSPoint(x: 42, y: 600), width: 410)
}

func drawClosing(_ p: CGFloat) {
  drawBase()
  NSColor(calibratedWhite: 0.06, alpha: 0.76 * ease(p)).setFill(); canvas.fill()
  let alpha = ease(p)
  text("86 PLACES · ONE CONNECTED HISTORY", in: NSRect(x: 250, y: 255, width: 700, height: 30), size: 14, color: NSColor.white.withAlphaComponent(alpha), weight: .bold, alignment: .center)
  text("Explore the map", in: NSRect(x: 200, y: 300, width: 800, height: 70), size: 46, color: NSColor.white.withAlphaComponent(alpha), weight: .bold, alignment: .center)
  text("Migration · work · worship · community · burial · remembrance", in: NSRect(x: 230, y: 382, width: 740, height: 35), size: 17, color: NSColor.white.withAlphaComponent(alpha), alignment: .center)
  roundedRect(NSRect(x: 475, y: 449, width: 250, height: 48), radius: 24, fill: red.withAlphaComponent(alpha))
  text("Victorian Chinese Heritage", in: NSRect(x: 475, y: 464, width: 250, height: 24), size: 14, color: NSColor.white.withAlphaComponent(alpha), weight: .bold, alignment: .center)
}

func makeFrame(_ spec: FrameSpec) -> CGImage? {
  let image = NSImage(size: canvas.size, flipped: true) { _ in
    switch spec.scene {
    case .opening: drawOpening(spec.progress)
    case .chronology: drawChronology(spec.progress)
    case .search: drawSearch(spec.progress)
    case .focus: drawFocus(spec.progress)
    case .detail: drawDetail(spec.progress)
    case .route: drawRoute(spec.progress)
    case .closing: drawClosing(spec.progress)
    }
    return true
  }
  var rect = canvas
  return image.cgImage(forProposedRect: &rect, context: nil, hints: [.interpolation: NSImageInterpolation.high])
}

var frames: [FrameSpec] = []
func transition(_ scene: Scene, steps: Int = 7, hold: Double = 0.08) {
  for index in 0..<steps {
    frames.append(FrameSpec(scene: scene, progress: CGFloat(index) / CGFloat(max(1, steps - 1)), delay: index == steps - 1 ? hold : 0.09))
  }
}
transition(.opening, steps: 4, hold: 1.2)
transition(.chronology, hold: 1.0)
transition(.search, hold: 0.9)
transition(.focus, hold: 0.9)
transition(.detail, steps: 9, hold: 1.5)
transition(.route, steps: 10, hold: 1.2)
transition(.closing, steps: 7, hold: 1.8)

guard let destination = CGImageDestinationCreateWithURL(outputURL as CFURL, UTType.gif.identifier as CFString, frames.count, nil) else {
  fputs("Could not create GIF destination.\n", stderr)
  exit(1)
}

CGImageDestinationSetProperties(destination, [
  kCGImagePropertyGIFDictionary: [kCGImagePropertyGIFLoopCount: 0]
] as CFDictionary)

for spec in frames {
  guard let frame = makeFrame(spec) else { continue }
  CGImageDestinationAddImage(destination, frame, [
    kCGImagePropertyGIFDictionary: [kCGImagePropertyGIFDelayTime: spec.delay]
  ] as CFDictionary)
}

guard CGImageDestinationFinalize(destination) else {
  fputs("Could not finalise GIF.\n", stderr)
  exit(1)
}

print("Created \(outputURL.path) with \(frames.count) frames")
