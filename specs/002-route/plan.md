# แผนงานสำหรับ SPEC-ROUTE

## 1. สรุปแนวทาง
ฟีเจอร์นี้สร้างระบบรับงานตามเส้นทางให้ซาเล้งเห็นรายชื่อผู้ขายที่อยู่ใกล้ที่สุดตามเส้นทางจริงที่ซาเล้งจะเดินทางภายในรัศมี 5 กม. โดยรวมข้อมูลจากพิกัด GPS, Maps Routing API, สถานะคำขอ, และกระบวนการยืนยันตัวตนก่อนเปิดเผยพิกัดที่ละเอียด จึงช่วยให้ซาเล้งวางแผนเดินทางได้เร็วและลดการขับรถเปล่า ส่วนผู้ขายได้รับประสบการณ์การดูงานที่รวดเร็วและโปร่งใส ตาม REQ-FN-002, REQ-SEC-002, REQ-BR-002 และ NFR ใน spec

โฟลเดอร์และโครงสร้างจะเริ่มจากโครงสร้างพื้นฐานของแอป/บริการตาม tech stack ที่ทีมจะเลือกต่อไป โดยคำนึงว่า feature นี้ครอบคลุมเพียง UC-04 และไม่ขยายไปถึง non-goals ที่ระบุไว้ใน spec

## 2. เทคโนโลยีที่ใช้
| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Frontend: React + Vite + Tailwind CSS | ทีมเลือกเอง ไม่ได้มาจาก spec | เลือกใช้สำหรับหน้าแอปผู้ใช้งานและส่วนติดต่อกับ API ได้เร็วและสะดวกต่อการสร้าง UI สำหรับงานตามเส้นทาง |
| Backend: FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับ REST API, validation, business logic, และเชื่อมต่อกับ Maps/GPS/Verification service |
| Database: PostgreSQL | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้เก็บข้อมูลผู้ใช้งาน, สถานะงาน, พิกัด, และประวัติยืนยันตัวตนพร้อมความเหมาะสมต่อ query เชิงพื้นที่และข้อมูลเชิงสัมพันธ์ |
| โครงโฟลเดอร์เริ่มต้น: `frontend/src/`, `backend/app/`, `backend/services/`, `backend/models/`, `db/`, `tests/` | ทีมเลือกเอง ไม่ได้มาจาก spec | แยก frontend/backend ให้ชัดเจนเพื่อให้ T-01 สร้าง project structure ได้ตรงตาม stack ที่เลือก |
| Maps Routing API / Geospatial service | REQ-CON-002 | ใช้เพื่อคำนวณ route distance, filter ตามรัศมี 5 กม., และจัดเรียงงานตามเส้นทางจริง |
| GPS + geolocation client | REQ-OP-002, AS-03 | ใช้สำหรับจัดเก็บพิกัดซาเล้งและตรวจสอบความคลาดเคลื่อนตามค่า accuracy ของอุปกรณ์ |
| Verification service Thai-ID / DBD-ID | SC-04 | ใช้ในกระบวนการยืนยันตัวตนก่อนเปิดเผยข้อมูลละเอียดและก่อนอนุมัติรับงาน |

หมายเหตุ: Stack นี้เป็นการตัดสินใจของทีมที่เลือกไว้แล้ว และใช้ร่วมกับฟีเจอร์นี้ โดยยังคงยึดข้อกำหนดจาก spec เป็นหลัก ไม่เพิ่มขอบเขตใหม่

## 3. โมเดลข้อมูล
| Entity / Object | ฟิลด์หลัก | รองรับ FR/REQ |
|---|---|---|
| ScrapRequest | id, status, geoPoint, scrapType, estimatedPrice, createdAt, acceptedBy, acceptedAt | REQ-FN-001, REQ-BR-002, REQ-SEC-002 |
| SalengLocation | salengId, lat, long, timestamp, accuracy, routeContext | REQ-FN-002, REQ-OP-002, REQ-QA-002 |
| SellerProfile | sellerId, fullName, phone, address, verificationStatus | REQ-SEC-002, SC-04 |
| ServiceAddress | geoPoint, hiddenAddress, verifiedCoordinate | REQ-SEC-002, SC-04 |
| RouteCandidate | requestId, salengId, routeDistanceKm, ETA, sortingScore | REQ-FN-002, REQ-QA-002 |
| VerificationRecord | entityType, verificationMethod, status, verifiedAt | SC-04 |

ข้อควรระวัง: ควรหลีกเลี่ยงการเก็บข้อมูล PII เช่น phone, Thai-ID, DBD-ID ในฟิลด์ที่สามารถเปิดเผยก่อนผ่านกระบวนการยืนยันตัวตน ตาม REQ-PRV-001, REQ-PRV-002 และแนวทาง AS-04

## 4. API / หน้าจอ
| Component | รายละเอียด | รองรับ FR |
|---|---|---|
| GET /api/route/jobs | ดึงงานรับซื้อที่อยู่ภายในรัศมี 5 กม. ตามเส้นทางจริงของซาเล้ง พร้อมกรองสถานะที่ยังคงว่าง | REQ-FN-002 |
| POST /api/route/jobs/{id}/accept | สร้างการ accept สำหรับงานที่ยังว่าง และตรวจสอบ concurrent-safe แบบ First-come | REQ-BR-002 |
| GET /api/route/jobs/{id} | ดูรายละเอียดงานแบบมีความเป็นส่วนตัว: ซ่อนพิกัดละเอียดจนกว่าผ่านการยืนยันตัวตน | REQ-SEC-002 |
| POST /api/verification/verify | ส่ง Thai-ID / DBD-ID เพื่อยืนยันตัวตนก่อนเปิดเผยข้อมูลเต็ม | SC-04 |
| POST /api/location/update | อัปเดตตำแหน่งและค่า accuracy ของซาเล้ง | REQ-OP-002 |
| UI: หน้า “รายการงานตามเส้นทาง” | แสดงรายการที่เรียงตาม route distance และเช็คว่าเสร็จสิ้นภายใน <= 3 วินาที ในสภาวะข้อมูลทดสอบตาม NFR | REQ-QA-002 |

## 5. ตารางตรวจ Constraints
| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| REQ-CON-002 | ใช้เป็นข้อจำกัดในการเรียก Maps API ให้คำนวณ route distance และทำ quota/rate protection | ใช้แล้ว |
| REQ-CON-003 | ต้องคำนึงถึงน้ำหนักบรรทุกของยานพาหนะซาเล้งในกระบวนการเลือกงานเพื่อให้ไม่เกิดงานที่เกินความสามารถ | ใช้แล้ว |
| SC-04 | ใช้ในการออกแบบ verification flow และการยืนยันตัวตนก่อนเปิดเผยพิกัดบ้านเลขที่ | ใช้แล้ว |
| REQ-PRV-001 | ใช้เพื่อหลีกเลี่ยงการเก็บ/เปิดเผย phone PII ในส่วนที่ไม่จำเป็น | ใช้แล้ว |
| REQ-PRV-002 | ใช้เพื่อซ่อน ServiceAddress.geoPoint จนกว่าผ่าน verification | ใช้แล้ว |
| AS-02 | ใช้ในแผน concurrent accept: server-side First-come | ใช้แล้ว |
| AS-03 | ใช้ในการคำนวณ route distance และการจัดเรียงงานจากเส้นทางจริง | ใช้แล้ว |
| AS-04 | ใช้ในแผน privacy masking สำหรับพิกัดบ้านเลขที่ | ใช้แล้ว |
| AS-05 | ใช้ในการออกแบบ metric สำหรับ GPS accuracy ด้วยค่าจากอุปกรณ์ | ใช้แล้ว |
| AS-06 | ใช้ในการกำหนด metric เวลาการตอบกลับฝั่ง Backend สำหรับ latency test | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria
| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-04-01 | `test_AC_04_01_route_jobs_visible_within_5km` | ตรวจสอบว่ารายการงานที่อยู่ภายใน 5 กม. ตาม route distance ปรากฏในผลลัพธ์และรายการที่เกินรัศมีจะไม่ปรากฏ |
| AC-04-02 | `test_AC_04_02_route_sorting_by_distance` | ทดสอบการจัดเรียงงานตามระยะทางที่เส้นทางจริงให้ถูกต้องและมีค่าน้อยสุดก่อน |
| AC-04-03 | `test_AC_04_03_route_map_display` | ตรวจสอบว่าผู้ใช้เห็นข้อมูลที่เหมาะสมบนแผนที่/รายการงาน โดยพิกัดที่ไม่เปิดเผยยังคงถูกซ่อนตามพฤติกรรมที่กำหนด |
| AC-04-04 | `test_AC_04_04_price_reference_display` | ตรวจสอบว่าราคาประเมินและราคากลางอ้างอิงแสดงอย่างถูกต้องในงานแต่ละรายการ |
| AC-04-05 | `test_AC_04_05_single_assignee_guard` | ทดสอบ concurrent accept โดยมีสองซาเล้งกดรับงานพร้อมกัน ให้สิทธิ์ไปที่ Request ที่ถึง Server ก่อนเท่านั้น |
| AC-04-06 | `test_AC_04_06_gps_accuracy_threshold` | ทดสอบว่าความคลาดเคลื่อน GPS ไม่เกิน 15% เมื่อคำนวณด้วย accuracy ของอุปกรณ์ร่วมกับ route distance |
| AC-04-07 | `test_AC_04_07_route_response_latency` | วัด response time ของ API หรือ service ที่คืนงานให้ซาเล้งในสภาพที่มีข้อมูลทดสอบภายใน 5 กม. ให้ภายใน 3 วินาที |
| AC-04-08 | `test_AC_04_08_address_hidden_until_accept` | ทดสอบว่าพิกัดบ้านเลขที่ถูกซ่อนจนกว่าซาเล้งกดรับงานและยืนยันตัวตนแล้วเท่านั้น |

## 7. ลำดับงาน
1. กำหนด contract ข้อมูลและ state สำหรับ `ScrapRequest`, `SalengLocation`, `ServiceAddress`, และ `VerificationRecord` (รองรับ REQ-FN-002, REQ-SEC-002, SC-04)
2. สร้าง service คำนวณ route distance และ filter รายการงานภายใน 5 กม. พร้อมจัดเรียงตามเส้นทางจริง (รองรับ REQ-FN-002, AS-03)
3. สร้าง API ดึงรายการงานตามเส้นทางและ API อัปเดตตำแหน่งซาเล้ง (รองรับ REQ-FN-002, REQ-OP-002)
4. เพิ่มการป้องกัน concurrent accept ที่ backend ด้วย policy First-come และตรวจสอบสถานะคำขอ (รองรับ REQ-BR-002, AS-02)
5. ปรับข้อมูลและ UI ให้ซ่อนพิกัดบ้านเลขที่จนกว่าจะยืนยันตัวตนและรับงาน (รองรับ REQ-SEC-002, SC-04, AS-04)
6. ปรับแสดงข้อมูลราคากลางและ GST/metadata ที่เกี่ยวข้อง (รองรับ REQ-FN-001)
7. ทดสอบ NFR ความแม่นยำและ latency ตาม AC-04-06, AC-04-07
8. ทดสอบ end-to-end สำหรับ AC-04-01 ถึง AC-04-08 และตรวจสอบว่าฝ่าย non-goal ยังไม่ถูกครอบคลุม (ตาม spec)

## 8. สิ่งที่ยังไม่ทำ
- AS-01: “ซาเล้งไม่น้อยกว่า 70% มีสมาร์ทโฟนรองรับ GPS และใช้แอปเป็น” — ยังต้องถาม/ยืนยันจาก RE Lead หรือทีมวิจัยก่อนวางแผนการสำรวจจริง
- Q-01: “กรณีซาเล้ง 2 คนกดรับงานพร้อมกันในเสี้ยววินาทีเดียวกัน” — ขณะนี้ยังไม่มีคำตอบยืนยันรูปแบบการตัดสินใจแน่นอนนอกจากการสรุปเป็น First-come ใน AS-02
- Q-02: “ควรคำนวณรัศมี 5 กม. จากระยะทางตรงหรือเส้นทางจริง?” — ขณะนี้มีคำตอบเป็น route distance ใน AS-03 แต่ยังต้องยืนยันกับทีมและผู้มีส่วนได้เสียก่อนจบให้เป็นข้อสรุปสุดท้าย
- Q-03: “การยืนยันตัวตน Thai-ID / DBD-ID จะเกิดก่อนหรือหลังรับงาน?” — ยังต้องยืนยันจาก Product/Compliance ก่อนวาง flow แบบสุดท้าย
- Q-04: “ค่า <= 3 วินาที ต้องวัดจากจุดไหนและเงื่อนไขอะไร?” — ยังต้องกำหนดสภาพแวดล้อมและตัวแปรวัดก่อนทดสอบจริง

หมายเหตุ: ข้อเหล่านี้จะยังไม่ถูก implement จนกว่าจะได้รับคำตอบจากทีมตาม spec
