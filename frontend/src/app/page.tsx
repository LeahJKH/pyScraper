'use client';

import { useState } from 'react';
import styles from './page.module.css';

type Job = {
  company_info: string[];
  link: string;
  title: string;
};

export default function Home() {
  const [showForm, setShowForm] = useState(false);
  const [location, setLocation] = useState('');
  const [query, setQuery] = useState('');
  const [jobs, setJobs] = useState<Job[]>([]);

  const fetchJobs = async (query: string, locations: string[]) => {
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
      console.log(data.jobs);
      setJobs(data.jobs);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    }
  };

  const handleSearch = () => {
    if (location.trim() && query.trim()) {
      fetchJobs(query.trim(), [location.trim()]);
    } else {
      alert('Please fill in both fields before searching.');
    }
  };

  return (
    <main className={styles.main}>
      <button onClick={() => setShowForm(true)}>finn.no</button>

      {showForm && (
        <section>
          <input
            type="text"
            placeholder="Enter location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <input
            type="text"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={handleSearch}>Search</button>
        </section>
      )}

      <section>
        {jobs.map((job, index) => (
          <div key={index}>
            <h2>{job.company_info[0]}, {job.company_info[1]}</h2>
            <a href={job.link} target="_blank" rel="noopener noreferrer">
              link til annonse
            </a>
            <p>{job.title}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
