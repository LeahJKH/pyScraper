'use client';

import { useState } from 'react';
import styles from './main.module.css';
import Image from 'next/image';

type Job = {
  company_info: string[];
  link: string;
  title: string;
  image?: string;
};

export default function Home() {
  const [showForm, setShowForm] = useState(false);
  const [location, setLocation] = useState('');
  const [query, setQuery] = useState('');
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchJobs = async (query: string, locations: string[]) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, locations }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        console.error('Backend error:', data.error);
        alert(data.error);
        setJobs([]);
      } else {
        setJobs(data.jobs || []);
      }
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
      alert('Something went wrong while fetching jobs.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (location.trim() && query.trim()) {
      setJobs([]); // Clear old jobs while loading
      fetchJobs(query.trim(), [location.trim()]);
    } else {
      alert('Please fill in both fields before searching.');
    }
  };

  return (
    <main className={styles.main}>
      <button onClick={() => setShowForm(true)} className={styles.sitebtn}>finn.no</button>

      {showForm && (
        <section className={styles.searchCont}>
          <input className={styles.inputFields}
            type="text"
            placeholder="Enter location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <input className={styles.inputFields}
            type="text"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={handleSearch} disabled={!location.trim() || !query.trim() || loading} className={styles.btnloader}>
            {loading ? 'Loading...' : 'Search'}
          </button>
        </section>
      )}

    <section className={styles.jobCont}>
      {jobs.map((job, index) => (
        <div key={index} className={styles.jobCard}>
          {job.image && (
            <Image
              src={job.image}
              alt="Company logo"
              width={150}
              height={80}
              style={{ objectFit: 'contain' }}
            />
          )}
          <h2>{job.company_info.length ? job.company_info.join(', ') : 'Unknown Company'}</h2>
          <a href={job.link} target="_blank" rel="noopener noreferrer">
            Link to ad
          </a>
          <p>{job.title}</p>
        </div>
      ))}
    </section>
    </main>
  );
}
