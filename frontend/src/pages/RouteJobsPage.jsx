import { useEffect, useMemo, useState } from 'react';
import { mockJobs } from '../data/mockJobs';
import JobCard from '../components/JobCard';

const defaultLat = 13.9630;
const defaultLng = 100.5953;

export default function RouteJobsPage() {
  const [jobs, setJobs] = useState(mockJobs);
  const [verifiedIds, setVerifiedIds] = useState([]);
  const [salengLocation, setSalengLocation] = useState({ lat: defaultLat, lng: defaultLng, accuracy: 12 });

  useEffect(() => {
    const loadJobs = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/route/jobs?lat=${salengLocation.lat}&lng=${salengLocation.lng}`
        );

        if (response.ok) {
          const data = await response.json();
          setJobs(data.jobs || mockJobs);
        }
      } catch (error) {
        setJobs(mockJobs);
      }
    };

    loadJobs();
  }, [salengLocation]);

  const visibleJobs = useMemo(
    () => jobs.filter((job) => job.distanceKm <= 5 || job.status === 'accepted').sort((a, b) => a.distanceKm - b.distanceKm),
    [jobs]
  );

  const handleVerify = async (jobId) => {
    try {
      const response = await fetch('http://localhost:8000/api/verification/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_id: jobId,
          saleng_id: 'saleng-01',
          method: 'thai_id',
          id_number: '1234567890123',
        }),
      });

      if (response.ok) {
        setVerifiedIds((current) => [...new Set([...current, jobId])]);
      }
    } catch (error) {
      setVerifiedIds((current) => [...new Set([...current, jobId])]);
    }
  };

  const handleAccept = async (jobId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/route/jobs/${jobId}/accept`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          saleng_id: 'saleng-01',
          lat: salengLocation.lat,
          lng: salengLocation.lng,
          accuracy_m: salengLocation.accuracy,
        }),
      });

      if (response.ok) {
        setJobs((current) =>
          current.map((job) => (job.id === jobId ? { ...job, status: 'accepted' } : job))
        );
      }
    } catch (error) {
      setJobs((current) =>
        current.map((job) => (job.id === jobId ? { ...job, status: 'accepted' } : job))
      );
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-600">
                Route jobs
              </p>
              <h1 className="mt-2 text-3xl font-bold text-slate-900">รายการรับซื้อขยะตามเส้นทาง</h1>
            </div>

            <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
              รัศมี 5 กม. • ความแม่นยำ GPS {salengLocation.accuracy} m
            </div>
          </div>
        </header>

        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">งานที่แสดง</p>
            <p className="mt-2 text-3xl font-bold text-slate-900">{visibleJobs.length}</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">รัศมี</p>
            <p className="mt-2 text-3xl font-bold text-slate-900">≤ 5 กม.</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">เวลา response</p>
            <p className="mt-2 text-3xl font-bold text-emerald-600">&lt; 3s</p>
          </div>
        </div>

        <div className="grid gap-5">
          {visibleJobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              verified={verifiedIds.includes(job.id)}
              onAccept={handleAccept}
              onVerify={handleVerify}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
