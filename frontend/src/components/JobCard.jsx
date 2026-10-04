export default function JobCard({ job, onAccept, onVerify, verified }) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-600">
            {job.status === 'accepted' ? 'มีผู้รับงานแล้ว' : 'พร้อมรับงาน'}
          </p>
          <h3 className="mt-2 text-xl font-bold text-slate-900">{job.scrapType}</h3>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">
          {job.distanceKm.toFixed(1)} กม.
        </span>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">ราคาประเมิน</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">{job.estimatedPrice} บาท</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">ราคาอ้างอิง</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">{job.priceRange}</p>
        </div>
      </div>

      <div className="mt-4 rounded-xl bg-slate-50 p-3">
        <p className="text-xs uppercase tracking-wide text-slate-500">สถานที่</p>
        <p className="mt-1 text-sm text-slate-700">
          {verified ? job.address : job.hiddenAddress}
        </p>
      </div>

      <div className="mt-5 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => onAccept(job.id)}
          disabled={job.status === 'accepted'}
          className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {job.status === 'accepted' ? 'รับงานแล้ว' : 'รับงาน'}
        </button>

        <button
          type="button"
          onClick={() => onVerify(job.id)}
          className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
        >
          ยืนยันตัวตน
        </button>
      </div>
    </article>
  );
}
